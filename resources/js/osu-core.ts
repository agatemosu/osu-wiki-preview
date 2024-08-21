import { ClickMenu } from "@/core/click-menu.ts";
import { MobileToggle } from "@/core/mobile-toggle.ts";
import { Nav } from "@/core/nav.ts";
import { StickyHeader } from "@/core/sticky-header.ts";
import { Tooltips } from "@/core/tooltips.ts";

export class OsuCore {
	clickMenu: ClickMenu;
	mobileToggle: MobileToggle;
	nav: Nav;
	stickyHeader: StickyHeader;
	tooltips: Tooltips;

	constructor() {
		this.clickMenu = new ClickMenu();
		this.mobileToggle = new MobileToggle();
		this.nav = new Nav(this);
		this.stickyHeader = new StickyHeader();
		this.tooltips = new Tooltips();
	}
}
