if (!window.hasInitializedSocket) {
    const audio = new Audio("{{ FORCE_SCRIPT_NAME }}/sounds/notification_default.wav");
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const socket = new WebSocket(`${wsProtocol}//` + window.location.host + "{{ FORCE_SCRIPT_NAME }}/ws/admin/notifications/");
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log(data);
    };
    socket.onopen = ()=>{
        socket.send('{"1": 234}');
    };
}