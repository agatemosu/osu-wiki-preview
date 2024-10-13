import { addGlobalEventListener } from "@/utils/event-listener.ts";

const activeClass = "js-mobile-toggle--active";

export class MobileToggle {
	constructor() {
		addGlobalEventListener("click", ".js-mobile-toggle", this.toggle);
	}

	toggle = (_: MouseEvent, button: HTMLElement) => {
		const targetId = button.dataset.mobileToggleTarget;

		if (targetId == null) return;

		const target = document.querySelector(
			`.js-mobile-toggle[data-mobile-toggle-id=${targetId}]`,
		);

		if (!(target instanceof HTMLElement)) return;

		const toActive = !button.classList.contains(activeClass);

		button.classList.toggle(activeClass, toActive);
		target.classList.toggle("hidden-xs", !toActive);
	};
}
