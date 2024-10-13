export function addGlobalEventListener<K extends keyof DocumentEventMap>(
	type: K,
	selectors: string,
	listener: (e: DocumentEventMap[K], target: HTMLElement) => void,
) {
	document.addEventListener(type, (e) => {
		if (!(e.target instanceof HTMLElement)) return;

		const target = e.target.closest(selectors);

		if (!(target instanceof HTMLElement)) return;

		listener(e, target);
	});
}
