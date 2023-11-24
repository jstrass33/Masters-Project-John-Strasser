<html>
  
    <head>
      <title>John's Data Center Tool</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
      <link rel="shortcut icon" href="favicon.ico"/>
      <link rel="shortcut icon" href="{{ url_for('static', filename='logo.ico')}}"/>
    </head>
  
<script>

  function loading(){
    const element = document.getElementById("submit");
    const span = document.createElement("span");
    
    span.classList.add("spinner-border"); 
    span.classList.add("spinner-border-sm"); 
    
    element.innerHTML = "Loading...    ";
    element.appendChild(span);
    
  }
  function loading2(){
    const element = document.getElementById("submit2");
    const span = document.createElement("span");
    span.classList.add("spinner-border"); 
    span.classList.add("spinner-border-sm"); 
    element.innerHTML = "Loading...    ";
    element.appendChild(span);
  }
  function loading3(){
    const element = document.getElementById("approvals");
    const span = document.createElement("span");
    span.classList.add("spinner-border"); 
    span.classList.add("spinner-border-sm"); 
    element.innerHTML = "Loading...    ";
    element.appendChild(span);
  }

</script>
<body>
 
  <div class="jumbotron text-center bg-dark text-white" style="padding-top: 25px;">
   
    <img src="{{ url_for('static', filename='logo.jfif')}}">

<h1 style="padding-top: 40px;">John's Switch Info App</h1>

</div>
<h4 style="text-align: center;"> Enter the IP Address of the Switch:</h4>
<form name="myForm" action="/" method="post" style="text-align: center;">
  <div class="form-group">

    <input type="text" name="IP" id="IP" />
    <br/>
  
  <div class="form-group form-check"></div>
    <button type="submit" name="submit" id="submit" class="btn btn-primary" value="Get Switch Info" onclick="loading()">Get Switch Info</button>
</div>
<div class="jumbotron text-center">
<h4>If you are unaware of the IP address of the Switch you are looking for, search for it by site below:</h4>
</div>
<div class="form-group">
  <label for="sel1">Select Site From List:</label>
  <select class="form-control" id="sel1" name="sel1" style="text-align: center;">
    
    <option>John's Data Center</option>
    <option>Other Data Center</option>
    
  </select>
</div>
<div class="form-group form-check"></div>
    <button type="submit" name="siteresponse" id="siteresponse" class="btn btn-primary" value="Show Switches From Site" onclick="loading2()">Show Devices From Site</button>
</div>


</form>

<!--
<script>
function validateForm() {
  let x = document.forms["myForm"]["username"].value;
  if (x == "") {
    alert("Username must be filled out");
    return false;
  }
  let y = document.forms["myForm"]["password"].value;
  if (x == "") {
    alert("Password must be filled out");
    return false;
  }
  let z = document.forms["myForm"]["IP"].value;
  if (z == "") {
    alert("IP address must be filled out");
    return false;
  }
}
</script>
-->
</body>
</html>
