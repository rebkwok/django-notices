(
    function () {
        const clear = document.getElementById('noticesClear');
        if (clear) {
            document.cookie = "notices_seen=; Max-Age=-99999999;"
            clear.remove()
        };
    }
)();

var noticesCookie = {
    createCookie: function (value, timeout_seconds) {
        var date = new Date(),
        expires = '';
        if (timeout_seconds) {
        date.setTime(date.getTime() + (timeout_seconds * 1000));
        expires = "; expires=" + date.toGMTString();
        } else {
        expires = "";
        }
    
        var secureString = "";
        if (window.isSecureContext) {
        secureString = "; Secure";
        }
    
        document.cookie = "notices_seen" + "=" + value + expires + "; path=/" + secureString;
    },
    
    setCookie: function (version, timeout_seconds) {
        this.createCookie(version, timeout_seconds);
        this.hidenoticedModal()
    },
    
    hidenoticedModal: function () {       
        document.getElementById('noticesModal').remove();
        document.getElementById('noticesModalFader').remove();
    },
};
