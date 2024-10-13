import type { ClickMenuCurrent } from "@/core/click-menu.ts";
import type { OsuCore } from "@/osu-core.ts";

interface CustomEventMap {
	"click-menu:current": CustomEvent<ClickMenuCurrent>;
}

declare global {
	interface Document {
		addEventListener<K extends keyof CustomEventMap>(
			type: K,
			listener: (this: Document, ev: CustomEventMap[K]) => void,
		): any;

		dispatchEvent<K extends keyof CustomEventMap>(ev: CustomEventMap[K]): any;
	}

	interface Window {
		osuCore: OsuCore;
	}
}
