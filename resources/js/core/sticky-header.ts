const pinnedClass = "js-header-is-pinned";

export class StickyHeader {
	constructor() {
		document.addEventListener("scroll", this.onScroll);
	}

	get shouldPin() {
		return window.scrollY > 30;
	}

	onScroll = () => {
		document.body.classList.toggle(pinnedClass, this.shouldPin);
	};
}
