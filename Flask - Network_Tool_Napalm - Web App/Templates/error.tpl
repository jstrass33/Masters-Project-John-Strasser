<html>
  <head>
    <title>John's Data Center Tool</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <link rel="shortcut icon" href="{{ url_for('static', filename='logo.ico')}}"/>
  </head>

<body onload="showincolor()">
  <!--<button type="button" id="btnSave" onclick="save()" class="button" style="display:block;
  margin:0 auto;">Download Copy of Switch Ports</button> -->
<div class="jumbotron text-center bg-dark text-white" style="padding-top: 25px;">
  <div style="float: left; padding-top: 0px;">
    <button type="button" name="submit" id="approvals" class="btn btn-primary" value="See Pending Approvals" onclick="loading3()"><a href="/" style="color: white;">Home</a></button>
    </div>
    <img src="{{ url_for('static', filename='logo.jfif')}}" style="margin-right: 50px;">
  <h1 style="text-align: center;">{{error}}</h1>
</div>
  
</body>
</html>
