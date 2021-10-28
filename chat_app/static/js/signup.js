
$("#signup").attr({"disabled":true})
function validateEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function button(type){
  if (type == "enable"){
    $("#signup").attr({"disabled":false})
  } else {
       $("#signup").attr({"disabled":true})
  }
}

$("#email").keyup(function(){
  if(validateEmail(this.value)){
    button("enable");
    $(this).addClass("text-success").removeClass("text-danger")
  } else{
    button("disable");
    $(this).removeClass("text-sucess").addClass("text-danger")
  }
})

$("#c_pass").keyup(function(){
  if ($(this).val() != $("#password").val() ){
    button("disable")
    $(this).addClass("text-danger").removeClass("text-success")
  } else{
    button("enable")
      $(this).addClass("text-success").removeClass("text-danger")
  }
})


$("#signup").click(function(){
  let first_name = $("#first_name").val();
  let email = $("#email").val();
  let password = $("#password").val();
  let usr = $("#username").val();
  let username = usr.replace(/ /g,"")
  let last_name = $("#last_name").val();
  let csrf = $("input[name='csrfmiddlewaretoken']").val();
 if (username < 5){
   $("#statusMsgs").text("Username should more than 5 characters");
  $(window).scrollTop();
   return
   
 }

  
  if (email == ""){
    $("#statusMsgs").text("Email is required");
    $(window).scrollTop();
    return
  }
    if(first_name == ""){
 
     $("#statusMsgs").text("First Name is Required");
     $(window).scrollTop();
    return
  }
  
  if (password == ""){
     $("#statusMsgs").text("password Cannot be blank..")
     $(window).scrollTop();
    return 
  }
  
  if(password.length < 5){
     $("#statusMsgs").text("password length should be more than 5 characters.")
     $(window).scrollTop();
     
    return 
  }
 
 if ($("#c_pass").val() != password){
    $("#statusMsgs").text("password didn't match..")
    $(window).scrollTop();
   return 
 }
  
 let signupData = {"username":username.toLowerCase(), "first_name":first_name,"email":email.toLowerCase(),"password":password,"csrfmiddlewaretoken":csrf,"last_name":last_name}
  $("#statusMsgs").removeClass("text-danger").addClass("text-info").text("Plaese wait...")
  $.ajax({
    url : "/accounts/signup/",
    method : "POST",
    data : signupData,
    success : function(resp){
      
      if(resp["status"]) {
          $("#statusMsgs").removeClass("text-danger text-info").addClass("text-success").text("Account is Created please Check your Email for Activate your account.. redirecting to login page..");
          
        setTimeout(function (){
          window.location.href="/accounts/login/"
        },3000)
      } else{
        $("#statusMsgs").text("This Email or username already Exists.. Try Again")
      }
    } // Success function ends here..
  })
  
})
