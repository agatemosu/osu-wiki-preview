// @ts-check

import { fadeIn, fadeOut } from "./utils/fade.js";

/**
 * @param {HTMLElement} button
 * @param {HTMLElement} menu
 */
export function openClickMenu(button, menu) {
	setMenuActive(menu);
	setButtonActive(button);
}

/**
 * @param {HTMLElement} button
 * @param {HTMLElement} menu
 */
export function closeClickMenu(button, menu) {
	setMenuInactive(menu);
	setButtonInactive(button);
}

/**
 * @param {HTMLElement} menu
 */
export function setMenuActive(menu) {
	fadeIn(menu);
	menu.classList.add("js-click-menu--active");
}

/**
 * @param {HTMLElement} menu
 */
export function setMenuInactive(menu) {
	fadeOut(menu);
	menu.classList.remove("js-click-menu--active");
}

/**
 * @param {HTMLElement} button
 */
export function setButtonActive(button) {
	button.classList.add("js-click-menu--active");
}

/**
 * @param {HTMLElement} button
 */
export function setButtonInactive(button) {
	button.classList.remove("js-click-menu--active");
}
