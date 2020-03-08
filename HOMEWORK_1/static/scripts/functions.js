function redirect_weather()
{
 	var days = document.getElementById("days").value;
	document.getElementById("buttonSubmit").onclick = function () {
        location.href = "/weather?days=" + days;
    };
}