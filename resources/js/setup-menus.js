// @ts-check

import { $, $$ } from "./utils.js";

const blackoutElement = /** @type {HTMLElement} */ ($(".js-blackout"));

/**
 * @param {HTMLElement} button
 */
function toggleClickMenu(button) {
	const clickMenuId = button.dataset.clickMenuTarget;

	const clickMenuTarget = $(`[data-click-menu-id="${clickMenuId}"]`);

	if (!clickMenuTarget) {
		return;
	}

	const isMenuVisible = clickMenuTarget.dataset.visibility === "visible";
	const newVisibility = isMenuVisible ? "hidden" : "visible";

	clickMenuTarget.dataset.visibility = newVisibility;
	clickMenuTarget.classList.toggle("js-click-menu--active");

	button.classList.toggle("js-click-menu--active");

	if (clickMenuId === "mobile-menu") {
		// In osu-web, it has an animation
		clickMenuTarget.style.display = isMenuVisible ? "none" : "block";

		document.body.classList.toggle("js-nav2--active");
		blackoutElement.dataset.visibility = newVisibility;
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
