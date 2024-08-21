import type { ClickMenu, ClickMenuCurrent } from "@/core/click-menu.ts";
import type { OsuCore } from "@/osu-core.ts";
import { blackoutToggle } from "@/utils/blackout.ts";
import { slideDown, slideUp } from "@/utils/slide.ts";

export class Nav {
	clickMenu: ClickMenu;
	showingMobileNav: boolean | undefined;

	constructor(core: OsuCore) {
		this.clickMenu = core.clickMenu;

		document.addEventListener("click-menu:current", this.autoMobileNav);
	}

	autoMobileNav = (e: CustomEvent<ClickMenuCurrent>) => {
		const { previousTree, target, tree } = e.detail;

		if (target === "mobile-menu") {
			this.clickMenu.show("mobile-nav");
			setTimeout(() => {
				const mobileMenu = this.clickMenu.menu("mobile-menu");
				if (!(mobileMenu instanceof HTMLElement)) return;

				for (const anim of mobileMenu.getAnimations()) anim.finish();

				slideDown(mobileMenu, 150);
			});
		}

		this.showingMobileNav = tree.indexOf("mobile-menu") !== -1;

		if (this.showingMobileNav) {
			document.body.classList.add("js-nav2--active");
			blackoutToggle(this, true);
			return;
		}

		if (previousTree.indexOf("mobile-menu") !== -1) {
			blackoutToggle(this, false);
			setTimeout(() => {
				const mobileMenu = this.clickMenu.menu("mobile-menu");
				if (!(mobileMenu instanceof HTMLElement)) return;

				for (const anim of mobileMenu.getAnimations()) anim.finish();

				slideUp(mobileMenu, 150, this.toggleActiveClass);
			});
		}
	};

	toggleActiveClass = () => {
		// use actual state instead of always removing the class in case
		// the menu is shown again right after it's closed
		document.body.classList.toggle("js-nav2--active", this.showingMobileNav);
	};
}
