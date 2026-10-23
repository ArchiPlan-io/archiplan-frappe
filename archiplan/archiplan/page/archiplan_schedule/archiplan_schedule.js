frappe.pages["archiplan-schedule"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({ parent: wrapper, title: __("ArchiPlan Schedule"), single_column: true });
    page.main.addClass("archiplan-schedule-page");
    if (!document.getElementById("archiplan-schedule-styles")) {
        const style = document.createElement("style");
        style.id = "archiplan-schedule-styles";
        style.textContent = `
            .archiplan-schedule-page { box-sizing: border-box; display: flex; min-height: 0; padding: var(--padding-md, 1rem); }
            .archiplan-schedule-page iframe { display: block; flex: 1; width: 100%; height: 100%; min-height: 0; border: 0; }
            .archiplan-empty { display: flex; flex: 1; flex-direction: column; align-items: center; justify-content: center; gap: 1rem; padding: var(--padding-lg, 1.5rem); text-align: center; }
        `;
        document.head.appendChild(style);
    }
    const setPageHeight = () => {
        window.requestAnimationFrame(() => {
            const top = page.main[0].getBoundingClientRect().top;
            page.main.css("height", `${Math.max(window.innerHeight - top, 0)}px`);
        });
    };
    setPageHeight();
    $(window).off("resize.archiplanSchedule").on("resize.archiplanSchedule", setPageHeight);
    frappe.call({
        method: "archiplan.archiplan.page.archiplan_schedule.archiplan_schedule.get_schedule_link",
        callback: ({ message }) => {
            if (message) {
                $("<iframe>", { src: message, title: __("ArchiPlan Schedule"), allow: "clipboard-read; clipboard-write" }).appendTo(page.main);
            } else {
                $("<div class='archiplan-empty'><p>" + __("Add a schedule link in ArchiPlan Settings to view your schedule.") + "</p><button class='btn btn-primary'>" + __("Open ArchiPlan Settings") + "</button></div>").appendTo(page.main).find("button").on("click", () => frappe.set_route("Form", "ArchiPlan Settings"));
            }
            setPageHeight();
        },
    });
};
