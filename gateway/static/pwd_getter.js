function getNewPassword(){
            var new_pw;
            var store = document.getElementsByName("store");
            //if(store[0].checked){ var storeOption = store[0]} else {var storeOption = store[1]}
            var kw = document.getElementsById("kw");

            var server_data = [
                {"storeOpt": storeOption},
                {"keyWord": kw}
            ];

            $.ajax({
                  type: "POST",
                  url: "/newpassword",
                  data: JSON.stringify(server_data),
                  contentType: "application/json",
                  dataType: 'json'
                  success: function(result) {
                        console.log("Result:");
                        console.log(result);
                  }
            });
}