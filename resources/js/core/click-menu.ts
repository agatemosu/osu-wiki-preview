import { addGlobalEventListener } from "@/utils/event-listener.ts";
import { fadeIn, fadeOut } from "@/utils/fade.ts";

export interface ClickMenuCurrent {
	previousTree: string[];
	target: string | null;
	tree: string[];
}

export class ClickMenu {
	private current: string | null = null;
	private documentMouseEventTarget: EventTarget | null = null;

	constructor() {
		addGlobalEventListener("click", ".js-click-menu--close", this.close);
		addGlobalEventListener(
			"click",
			".js-click-menu[data-click-menu-target]",
			this.toggle,
		);
		document.addEventListener("mousedown", this.onDocumentMousedown);
		document.addEventListener("mouseup", this.onDocumentMouseup);
	}

	close = () => {
		this.show();
	};

	closestMenuId = (child: Element | null) => {
		return child
			?.closest("[data-click-menu-id]")
			?.getAttribute("data-click-menu-id") ?? null;
	};

	menu = (id: string | null) => {
		return document.querySelector(
			`.js-click-menu[data-click-menu-id${id == null ? "" : `='${id}'`}]`,
		);
	};

	menuLink = (id: string | null) => {
		return document.querySelector(
			`.js-click-menu[data-click-menu-target${id == null ? "" : `='${id}'`}]`,
		);
	};

	show = (target: string | null = null) => {
		const previousTree = this.tree();

		this.current = target;

		const tree = this.tree();
		const menus = document.querySelectorAll(
			".js-click-menu[data-click-menu-id]",
		);

		let validCurrent = false;

		for (const menu of menus) {
			if (!(menu instanceof HTMLElement)) {
				continue;
			}

			const menuId = menu.dataset.clickMenuId ?? null;

			if (menuId == null || tree.indexOf(menuId) === -1) {
				fadeOut(menu);
				menu.classList.remove("js-click-menu--active");
				this.menuLink(menuId)?.classList.remove("js-click-menu--active");
			} else {
				fadeIn(menu);
				menu.classList.add("js-click-menu--active");
				this.menuLink(menuId)?.classList.add("js-click-menu--active");
				validCurrent = true;
			}
		}

		if (!validCurrent) {
			this.current = null;
		}

		const event = new CustomEvent<ClickMenuCurrent>("click-menu:current", {
			detail: { previousTree, target: this.current, tree },
		});

		document.dispatchEvent(event);
	};

	toggle = (e: MouseEvent, menu: HTMLElement) => {
		const tree = this.tree();

		e.preventDefault();

		const target = menu.dataset.clickMenuTarget;
		let next = target;

		if (target != null) {
			const index = tree.indexOf(target);

			if (index !== -1) {
				// toggling part of the menu tree, show parent of toggled menu
				next = tree[index + 1];
			}
		}

		this.show(next);
	};

	tree = () => {
		if (this.current == null) return [];

		let traverseId: string | null = this.current;
		const tree = [traverseId];

		for (;;) {
			traverseId = this.closestMenuId(this.menuLink(traverseId));

			if (traverseId == null) {
				break;
			}
			tree.push(traverseId);
		}

		return tree;
	};

	private readonly onDocumentMousedown = (e: MouseEvent) => {
		this.documentMouseEventTarget = e.button === 0 ? e.target : null;
	};

	private readonly onDocumentMouseup = (e: MouseEvent) => {
		if (this.documentMouseEventTarget !== e.target) return;
		if (e.button !== 0) return;
		if (this.current == null) return;
		if (!(e.target instanceof HTMLElement)) return;
		if (e.target.closest(".js-click-menu")) return;

		this.show();
	};
}
