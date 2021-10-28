 var socket = new WebSocket("ws://localhost:8000"+window.location.pathname)
 
 console.log(socket)
 
 $("#send_msg").click(function(){
  console.log("Msg sent.");
})




$(".msg_delete").click(function(){
  alert ("delete")
})



$("#save_edit").click(function(){
  
})