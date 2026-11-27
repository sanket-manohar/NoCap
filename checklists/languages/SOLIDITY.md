# Solidity / Smart Contracts — Security & Standards Checklist

## Checks and standard fixes
- [ ] **Reentrancy** → checks-effects-interactions; OpenZeppelin `ReentrancyGuard`
- [ ] **Access control** → OpenZeppelin `Ownable2Step`/`AccessControl`; never `tx.origin` for auth
- [ ] **Arithmetic** → Solidity ≥0.8 (checked math); careful with `unchecked`
- [ ] **External calls** → check return values; pull-over-push payments; gas limits
- [ ] **Oracles** → manipulation-resistant price feeds (TWAP, Chainlink); no spot price from a single DEX
- [ ] **Upgradeability** → initializers protected; storage layout checks; timelock + multisig for admin
- [ ] **Randomness** → never `block.timestamp`/`blockhash`; use VRF
- [ ] **Process** → full test suite + fuzzing (Foundry), static analysis, independent audit before mainnet, bug bounty

## Tools
Slither, Mythril, Foundry fuzz/invariant tests, Echidna, SWC registry.
