import { currentTimeInSeconds, round } from './timeUtils';

class DurationLogger {
  #timeThresholds;
  #currentTargetId;
  #startTime;
  #loggingProcess;

  /**
   *
   * @param {(targetId, duration)=>void} loggingProcess
   * @param {number} timeThresholds // in seconds
   */
  constructor(loggingProcess, timeThresholds) {
    this.#timeThresholds = timeThresholds;
    this.#loggingProcess = loggingProcess;
    this.#initialize();
  }

  #initialize() {
    this.#currentTargetId = null;
    this.#startTime = null;
  }

  #logging() {
    const duration = round(currentTimeInSeconds() - this.#startTime, 2);
    if (this.#currentTargetId !== null && duration > this.#timeThresholds) {
      this.#loggingProcess(this.#currentTargetId, duration);
    }
  }

  changeTarget(targetId) {
    if (this.#currentTargetId === targetId) return;
    this.#logging();
    this.#startTime = currentTimeInSeconds();
    this.#currentTargetId = targetId;
  }

  close() {
    this.#logging();
    this.#initialize();
  }
}

export default DurationLogger;
