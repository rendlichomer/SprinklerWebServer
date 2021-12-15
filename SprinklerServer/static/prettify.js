var ugly = document.getElementById("config").value;
var obj = JSON.parse(ugly);
var pretty = JSON.stringify(obj, undefined, 4);
document.getElementById("config").value = pretty;