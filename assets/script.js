if (!window.dash_clientside) {
  window.dash_clientside = {};
}
window.dash_clientside.clientside = {
  attach_vanta: function (id) {
    setTimeout(function () {
      const el = document.getElementById(id);
      VANTA.NET({
        el,
        mouseControls: true,
        touchControls: true,
        gyroControls: true,
        minHeight: 560.00,
        minWidth: 450.00,
        scale: 1.00,
        scaleMobile: 1.00,
        color: 0x707070,
        backgroundColor: 0x0,
        points: 20.00,
        spacing: 17.00
      });
    }, 1);
    return window.dash_clientside.no_update;
  },
};