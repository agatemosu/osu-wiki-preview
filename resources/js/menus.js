// @ts-check

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
	menu.dataset.visibility = "visible";
	menu.classList.add("js-click-menu--active");
}

/**
 * @param {HTMLElement} menu
 */
export function setMenuInactive(menu) {
	menu.dataset.visibility = "hidden";
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
