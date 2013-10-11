<!DOCTYPE html>
<html lang="en">
    <head>
    <title>{{ user.username }} | Friendly Island</title>
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

    <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <div class="page-header">
                <h1>Hey, {{ user.first_name }}</h1>
            </div>
            <div class="row">
                <div class="span8" id="user-apps">
                    %include profile_apps_table apps=apps
                </div>
            </div>
        </div>
        <!--Javascripts-->
        <script type="text/javascript" src="assets/js/jquery-1.10.2.min.js"></script>
        <script type="text/javascript" src="assets/js/bootstrap.min.js"></script>        
        <script type="text/javascript">
            function deleteApp(appID){
                $.post("delete_app", {appID: appID}, function( resp ){
                    $("#user-apps").html( resp );
                });
            }
        </script>
    </body>
</html>