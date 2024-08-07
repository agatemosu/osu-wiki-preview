// @ts-check

import { isVisible } from "./fade.js";
import { closeClickMenu, openClickMenu } from "./menus.js";
import { toggleNav, toggleNavTab } from "./nav.js";
import { $, $$ } from "./utils.js";

/**
 * @param {HTMLElement} button
 */
function toggleClickMenu(button) {
	const clickMenuId = button.dataset.clickMenuTarget;
	const clickMenuTarget = $(`[data-click-menu-id="${clickMenuId}"]`);

	if (!clickMenuTarget) {
		return;
	}

	if (button.classList.contains("mobile-menu-tab")) {
		toggleNavTab(button, clickMenuTarget);
		return;
	}

	const isMenuVisible = isVisible(clickMenuTarget);

	if (isMenuVisible) {
		closeClickMenu(button, clickMenuTarget);
	} else {
		openClickMenu(button, clickMenuTarget);
	}

	if (clickMenuId === "mobile-menu") {
		toggleNav(clickMenuTarget, isMenuVisible);
	}
}

/**
 * @param {HTMLElement} button
 */
function toggleMobileElement(button) {
	const mobileToggleId = button.dataset.mobileToggleTarget;

	const mobileToggleTarget = $(`[data-mobile-toggle-id="${mobileToggleId}"]`);

	if (!mobileToggleTarget) {
		return;
	}

	button.classList.toggle("js-mobile-toggle--active");
	mobileToggleTarget.classList.toggle("hidden-xs");
}

export function setupMenus() {
	const buttons = $$("[data-click-menu-target]");

	for (const button of buttons) {
		button.addEventListener("click", (event) => {
			toggleClickMenu(button);
			event.stopPropagation();
		});
	}
}

export function setupMobileMenus() {
	const buttons = $$("[data-mobile-toggle-target]");

	for (const button of buttons) {
		button.addEventListener("click", (event) => {
			toggleMobileElement(button);
			event.stopPropagation();
		});
	}
}
