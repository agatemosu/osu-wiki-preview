import "../css/app.less";

document.addEventListener("DOMContentLoaded", () => {
	const menuToggleButtons = document.querySelectorAll(
		".js-click-menu[data-click-menu-target]",
	);
	const mobileToggleButtons = document.querySelectorAll(
		".js-mobile-toggle[data-mobile-toggle-target]",
	);
	const blackoutElement = document.querySelector(".js-blackout");

	function toggleClickMenu(button) {
		const targetMenuId = button.getAttribute("data-click-menu-target");
		const targetedMenu = document.querySelector(
			`.js-click-menu[data-click-menu-id="${targetMenuId}"]`,
		);

		const isMenuVisible = targetedMenu.dataset.visibility === "visible";
		targetedMenu.dataset.visibility = isMenuVisible ? "hidden" : "visible";

		button.classList.toggle("js-click-menu--active");
		targetedMenu.classList.toggle("js-click-menu--active");

		if (targetMenuId === "mobile-menu") {
			blackoutElement.dataset.visibility = isMenuVisible ? "hidden" : "visible";
			document.body.classList.toggle("js-nav2--active");
			targetedMenu.style.display = isMenuVisible ? "none" : "block";
		}
	}

	function toggleMobileElement(button) {
		const targetToggleId = button.getAttribute("data-mobile-toggle-target");
		const targetedToggle = document.querySelector(
			`.js-mobile-toggle[data-mobile-toggle-id="${targetToggleId}"]`,
		);

		button.classList.toggle("js-mobile-toggle--active");
		targetedToggle.classList.toggle("hidden-xs");
	}

	for (const button of menuToggleButtons) {
		button.addEventListener("click", (event) => {
			toggleClickMenu(button);
			event.stopPropagation();
		});
	}

	for (const button of mobileToggleButtons) {
		button.addEventListener("click", () => {
			toggleMobileElement(button);
		});
	}
});

document.addEventListener("click", (event) => {
	const isClickInsideMenu = event.target.closest("[data-click-menu-id]");

	if (!isClickInsideMenu) {
		const visibleMenus = document.querySelectorAll(
			'.js-click-menu--active[data-visibility="visible"]',
		);
		for (const menu of visibleMenus) {
			menu.dataset.visibility = "hidden";
			menu.classList.remove("js-click-menu--active");
		}

		const activeButtons = document.querySelectorAll(
			".js-click-menu--active[data-click-menu-target]",
		);
		for (const button of activeButtons) {
			button.classList.remove("js-click-menu--active");
		}

		const activeBlackout = document.querySelector(
			'.js-blackout[data-visibility="visible"]',
		);

		if (activeBlackout) {
			activeBlackout.dataset.visibility = "hidden";
		}
		document.body.classList.remove("js-nav2--active");
	}
});

document.addEventListener("scroll", () => {
	document.body.classList.toggle("js-header-is-pinned", window.scrollY > 30);
});
