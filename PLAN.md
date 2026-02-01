# Project Plan for TradeGold

## Overview
The TradeGold project aims to automate and optimize trading workflows using integrations with APIs from IBKR (Interactive Brokers) and IG. The project will leverage programmatic trading strategies and provide tools for analytics, configuration management, and result tracking.

---

## Objectives
1. Integrate IBKR and IG APIs to enable automated trading.
2. Develop robust scripts for executing trades (`ibkr_scripts/`, `ig_scripts/`).
3. Implement configuration management for seamless project customization (`configs/`).
4. Establish a testing framework to ensure code reliability (`tests/`).
5. Build result tracking functionalities to log and review trading performance (`results/`).

---

## Timeline
1. **Phase 1 - API Integration (Month 1):**
   - Set up API authentication and basic connectivity for IBKR and IG.
   - Ensure reliable communication with both APIs.

2. **Phase 2 - Script Development (Months 2–3):**
   - Develop trading scripts for IBKR and IG with required logic.
   - Implement unit tests to validate script behavior.

3. **Phase 3 - Analytics and Results Tracking (Month 4):**
   - Set up result-logging scripts to save analytics in the `results/` directory.
   - Develop visual reporting tools for trading analysis.

4. **Phase 4 - Final Review and Deployment (Month 5):**
   - Perform a full system review (testing in `tests/`).
   - Deploy the project and ensure documentation is complete.

---

## Planned Features
1. Automated trading through IBKR and IG APIs.
2. Logs for analytics and backtesting.
3. Modular configurations for strategy parameters via `configs/`.

---

## Technical Stack
- **Programming Language**: Python.
- **Libraries**:
  - `ib_insync` for IBKR API.
  - `requests` for IG API communication.
  - `pandas` for data management.
- **Testing Framework**: Pytest.

---

## Tasks
- **API Integration**:
  - Connect TradeGold to IBKR and IG APIs.
- **Script Development**:
  - Write trading strategies for real-time execution.
- **Tests and Validation**:
  - Unit tests to ensure reliability and accuracy.
- **Analytics Setup**:
  - Tracking and storage of performance metrics.