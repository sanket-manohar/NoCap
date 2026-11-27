"""Tests for the NoCap scanner. Run: python3 -m unittest discover -s tests

Secret-looking fixtures are assembled at runtime so this repo never contains
strings that trip GitHub push protection or other secret scanners.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scanner"))
import nocap  # noqa: E402

J = "".join  # join helper to split secret-like literals


def build_project(files):
    root = tempfile.mkdtemp(prefix="vp-")
    for rel, content in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(content)
    return root


def rule_ids(root, **kw):
    sc = nocap.Scanner(root, **kw).scan()
    return {f["rule"] for f in sc.findings}, sc


VULN = {
    "package.json": json.dumps({"dependencies": {"express": "^4.19.0", "openai": "*", "@supabase/supabase-js": "^2"}}),
    "src/db.js": "const r = await pool.query(`SELECT * FROM users WHERE id = ${req.params.id}`);\n",
    "src/ai.js": "const client = new OpenAI({ apiKey: k, dangerouslyAllowBrowser: true });\n",
    "src/run.js": "exec(`git log ${req.query.ref}`);\n",
    "src/ui.jsx": "<div dangerouslySetInnerHTML={{__html: bio}} />\n",
    "src/auth.js": "localStorage.setItem('token', jwt);\nconst t = Math.random().toString(36); // reset token\n",
    "src/cfg.js": J(["const OPENAI = '", "sk-proj-", "A" * 48, "';\n"]),
    "src/env.js": "const k = process.env.NEXT_PUBLIC_OPENAI_API_KEY;\n",
    "src/aws.py": J(["KEY = '", "AKIA", "Z" * 16, "'\n"]),
    "app.py": ("import os, pickle, yaml, hashlib\n"
               "cursor.execute(f\"SELECT * FROM t WHERE name = '{name}'\")\n"
               "os.system('rm ' + path)\n"
               "data = pickle.loads(blob)\n"
               "cfg = yaml.load(open('c.yml'))\n"
               "h = hashlib.md5(pw.encode())\n"
               "requests.get(url, verify=False)\n"
               "DEBUG = True\n"),
    "Main.java": 'stmt.executeQuery("SELECT * FROM u WHERE id=" + id);\n',
    "main.go": 'db.Query(fmt.Sprintf("SELECT * FROM u WHERE id=%s", id))\ntls.Config{InsecureSkipVerify: true}\n',
    "index.php": "<?php echo $_GET['q']; mysqli_query($c, \"SELECT * FROM u WHERE id=\" . $_GET['id']); ?>\n",
    "app.rb": 'User.where("email = \'#{params[:email]}\'")\n',
    "x.c": "char b[8]; gets(b); strcpy(b, s);\n",
    "Dockerfile": "FROM node:latest\nENV API_SECRET=abc123456\nRUN curl https://x.sh | sh\n",
    "firestore.rules": "service cloud.firestore { match /{d=**} { allow read, write: if true; } }\n",
    "supabase/migrations/1.sql": "create table notes (id int);\nalter table notes disable row level security;\n",
    ".github/workflows/ci.yml": "on: issues\njobs:\n  a:\n    steps:\n      - run: echo \"${{ github.event.issue.title }}\"\n",
    "main.tf": 'resource "aws_s3_bucket" "b" { acl = "public-read" }\ningress { cidr_blocks = ["0.0.0.0/0"] }\n',
    "AndroidManifest.xml": '<application android:usesCleartextTraffic="true" android:allowBackup="true">\n',
    ".env": "DB_PASSWORD=supersecretvalue\n",
}


class TestDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = build_project(VULN)
        cls.ids, cls.sc = rule_ids(cls.root)

    def test_expected_rules_fire(self):
        expected = {
            "INJ001", "AI001", "INJ012", "XSS002", "WEB010", "CRY003", "SEC005", "SEC013", "SEC001",
            "INJ002", "INJ013", "DES001", "DES002", "CRY001", "TLS001", "WEB003", "INJ003", "INJ004",
            "XSS004", "INJ005", "INJ006", "MEM001", "IAC001", "IAC002", "IAC003", "IAC011", "BAAS001",
            "BAAS002", "IAC009", "IAC007", "IAC006", "MOB001", "MOB002", "HYG001", "HYG002", "DEP001",
            "HYG004", "HYG006",
        }
        missing = expected - self.ids
        self.assertFalse(missing, f"rules did not fire: {sorted(missing)}")

    def test_stack_detection(self):
        st = self.sc.stack()
        self.assertIn("Node.js", st["platforms"])
        self.assertIn("Express", st["frameworks"])
        self.assertIn("OpenAI SDK", st["frameworks"])
        self.assertIn("Supabase", st["frameworks"])
        self.assertIn("js", st["languages"])

    def test_secrets_redacted(self):
        for f in self.sc.findings:
            if f["rule"] in ("SEC001", "SEC005"):
                self.assertIn("redacted", f["snippet"])
                self.assertNotIn("Z" * 16, f["snippet"])

    def test_critical_caps_score(self):
        s = self.sc.score()
        self.assertLessEqual(s["overall"], 49)
        self.assertEqual(s["grade"] in ("D", "F"), True)

    def test_recommendations_match_stack(self):
        rec = self.sc.recommendations()
        self.assertIn("checklists/security/OWASP_LLM_TOP10_2025.md", rec["checklists"])
        self.assertIn("checklists/languages/PYTHON.md", rec["checklists"])
        self.assertIn("checklists/platforms/BAAS_SUPABASE_FIREBASE.md", rec["checklists"])

    def test_every_finding_has_fix(self):
        for f in self.sc.findings:
            self.assertTrue(f["fix"], f["rule"])
            self.assertTrue(f["owasp"], f["rule"])


class TestCleanProject(unittest.TestCase):
    def test_clean_project_scores_high(self):
        files = {
            "package.json": json.dumps({"dependencies": {"express": "^4.19.0"}}),
            "package-lock.json": "{}",
            ".gitignore": ".env*\nnode_modules\n",
            ".github/workflows/ci.yml": "on: push\npermissions:\n  contents: read\n",
            ".github/dependabot.yml": "version: 2\n",
            "src/db.js": "const r = await pool.query('SELECT * FROM users WHERE id = $1', [id]);\n",
            "test/db.test.js": "test('x', () => {});\n",
        }
        for doc in ["README.md", "LICENSE", "SECURITY.md", "CHANGELOG.md", "CONTRIBUTING.md"] + [
                f"docs/{d}.md" for d in ["ARCHITECTURE", "DESIGN", "MODULES", "API", "DATA_MODEL", "THREAT_MODEL",
                                         "COMPLIANCE", "PRIVACY", "TESTING", "DEPLOYMENT", "RUNBOOK"]]:
            files[doc] = "# doc\n"
        files["docs/adr/0001-record.md"] = "# ADR\n"
        ids, sc = rule_ids(build_project(files))
        self.assertEqual(ids, set(), ids)
        self.assertEqual(sc.score()["grade"], "A+")


class TestSuppressionAndPlaceholders(unittest.TestCase):
    def test_inline_ignore(self):
        ids, _ = rule_ids(build_project({"a.js": "el.innerHTML = x; // nocap-ignore XSS001\n",
                                         ".gitignore": "x"}))
        self.assertNotIn("XSS001", ids)

    def test_placeholder_not_flagged(self):
        ids, _ = rule_ids(build_project({"a.py": "password = os.environ['DB_PASSWORD']\napi_key = 'your-api-key-here'\n"}))
        self.assertNotIn("SEC012", ids)

    def test_real_hardcoded_password_flagged(self):
        ids, _ = rule_ids(build_project({"a.py": "db_password = 'Pr0d!Hunter2xx'\n"}))
        self.assertIn("SEC012", ids)

    def test_toolkit_dir_skipped(self):
        files = {".nocap/.nocap-toolkit": "", ".nocap/scanner/x.js": "eval(a)\n", "a.js": "ok\n"}
        ids, _ = rule_ids(build_project(files))
        self.assertNotIn("INJ010", ids)


class TestFileIgnoreAndNode(unittest.TestCase):
    def test_ignore_file_marker(self):
        ids, _ = rule_ids(build_project({"rules.py": "# nocap-ignore-file\nx = eval(y)\n"}))
        self.assertNotIn("INJ010", ids)

    def test_node_without_deps_needs_no_lockfile(self):
        ids, _ = rule_ids(build_project({"package.json": json.dumps({"name": "x", "bin": {"x": "x.js"}})}))
        self.assertNotIn("HYG004", ids)


class TestCLI(unittest.TestCase):
    def test_cli_outputs(self):
        root = build_project(VULN)
        js = os.path.join(root, "out.json")
        badge = os.path.join(root, "badge.svg")
        script = os.path.join(HERE, "..", "scanner", "nocap.py")
        r = subprocess.run([sys.executable, script, root, "--json", js, "--badge", badge, "--fail-on", "high", "--quiet"])
        self.assertEqual(r.returncode, 1)
        self.assertTrue(os.path.exists(os.path.join(root, "NOCAP_REPORT.md")))
        with open(js) as fh:
            data = json.load(fh)
        self.assertIn("score", data)
        with open(badge) as fh:
            self.assertIn("<svg", fh.read())
        r2 = subprocess.run([sys.executable, script, "--list-rules"], capture_output=True, text=True)
        self.assertIn("SEC001", r2.stdout)


if __name__ == "__main__":
    unittest.main()
