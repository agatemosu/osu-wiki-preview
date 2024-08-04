// @ts-check

/**
 * @param {string} selector
 * @returns {HTMLElement | null}
 */
export const $ = (selector) => document.querySelector(selector);

/**
 * @param {string} selector
 * @returns {NodeListOf<HTMLElement>}
 */
export const $$ = (selector) => document.querySelectorAll(selector);
