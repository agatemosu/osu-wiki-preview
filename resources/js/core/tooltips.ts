import dayjs from "dayjs";
import tippy from "tippy.js";

export class Tooltips {
	constructor() {
		const timeElements = document.querySelectorAll("time");

		for (const el of timeElements) {
			el.title = this.timeagoTip(el, el.title).outerHTML;
		}

		const elements = document.querySelectorAll("[title]");

		for (const el of elements) {
			if (!(el instanceof HTMLElement)) {
				continue;
			}

			if (el.title === "") {
				continue;
			}

			tippy(el, {
				content: el.title,
				allowHTML: true,
				delay: 100,
				duration: 200,
			});
			el.removeAttribute("title");
		}
	}

	timeagoTip = (el: HTMLTimeElement, title: string) => {
		const timeString = el.dateTime ?? title;
		const time = dayjs(timeString);

		const $dateEl = document.createElement("strong");
		$dateEl.textContent = time.format("D MMMM YYYY");

		const $timeEl = document.createElement("span");
		$timeEl.classList.add("tippy-box__time");
		$timeEl.textContent = `${time.format("HH:mm:ss")} ${this.tzString(time)}`;

		const $tipEl = document.createElement("span");
		$tipEl.append($dateEl);
		$tipEl.append(" ");
		$tipEl.append($timeEl);

		return $tipEl;
	};

	tzString = (time: dayjs.Dayjs) => {
		const offset = time.utcOffset();

		const offsetString =
			offset % 60 === 0
				? `${offset >= 0 ? "+" : ""}${offset / 60}`
				: time.format("Z");

		return `UTC${offsetString}`;
	};
}
