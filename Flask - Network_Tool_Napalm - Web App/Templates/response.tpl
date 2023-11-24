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
  <h1 id="title" style="text-align: center;">Switch {{hostname}}</h1>
  <h3 style="text-align: center;">{{uptime}}</h3>
</div>

{% if vlan != None %}
  <form action="/" method="post">
    <h4 style="text-align: center; color: black;"><strong>Interface: {{interface}} is currently set to VLAN: {{vlan}}</strong></h4>
    <div class="form-group" style="text-align: center;">
    <label id="vlanchangelabel" style="color: black;">Input the VLAN number below and click submit to initiate change request.</label>
   
    <input type="text" name="vlanchangenumber" id="vlanchangenumber" class="form-control" required/>
              
              <input type="hidden" name='forminterface' value={{interface}} />
    
              <input type="hidden" name='vlan' value={{vlan}} />
              <input type="hidden" name='ipaddress' value={{IP}} />
              <input type="hidden" name='formhostname' value={{hostname}} />
              <input type="hidden" name='formthisdict' value={{data}} />
              <input type="hidden" name='vendor' value={{vendor}} />
              <input type="hidden" name='version' value={{version}} />
              <input type="hidden" name='model' value={{model}} />
   
      
        <label id="vlanchangelabel" style="color: black;">Input a comment on why you are requesting a VLAN change.</label>
       
        <input type="textarea" name="changereason" id="changereason" class="form-control" required/>
        <br>
       
        <div style="text-align: center;">
    <button type="submit" name="submit2" id="submit2" class="btn btn-warning" onclick="loading()"><strong>Submit VLAN Change</strong></button>
    </div>
  </form>
{% endif %}

<br>

<table class="table"> 
<thead class="bg-primary text-white">
  <tr>
    <th>Vendor</th>
    <th>Version</th>
    <th>Model</th>
    <th>Serial Number</th>
  </tr>
  </thead>

  <tr>
      <td>{{vendor}}</td>
      <td>{{version}}</td>
      <td>{{model}}</td>
      <td>{{serial_number}}</td>

  </tr>

</table>


<br>

<table id='txtdata' class="table table-striped table-hover">
  <thead class="bg-primary text-white">
  <tr>
    <th>Interface</th>
    <th>Port Description</th>
    <th>Device Connected</th>
    <th>VLAN</th>
  </tr>
  </thead>
  
  {%for inter, interinfo in data.items() %}
  <form action="/" method="post">
    <tr >
      
      <td>{{inter}}
        <input type="hidden" name='forminterface' value={{inter}} />
      </td>
      {% for key in interinfo %}
        
          
         
          {%if key != 'Vlan' %}
            <td id='datarow' > {{interinfo[key]}} </td>

          {% else %}
            <td id='datarow' > {{interinfo[key]}} 

            <!-- Correct how it was before {{interinfo[key]}} -->
            
              <input type="hidden" name='vlan' value={{interinfo[key]}} />
              <input type="hidden" name='ipaddress' value={{IP}} />
              <input type="hidden" name='formhostname' value={{hostname}} />
              <input type="hidden" name='formthisdict' value={{data}} />
              <input type="hidden" name='vendor' value={{vendor}} />
              <input type="hidden" name='version' value={{version}} />
              <input type="hidden" name='model' value={{model}} />
              
              <input type="hidden" name='serial_number' value={{serial_number}} />
              
            
            <button class="btn btn-secondary" type="submit" name='changevlan' id='changevlan' style="float: right;"><Strong>Change VLAN</Strong></button>
            </form> 
            </td>
          {% endif %}
          <!-- </form> -->
   
          </div>
        </td>
      
      {% endfor %}
      
     </tr>

      
  </tr>
  
  {% endfor %}
</table>
<hr/>

<hr/>
<script>

function save() {
      var data = document.getElementById("txtdata").innerHTML;
      var c = document.createElement("a");
      var asaname = '{{hostname}}';
      /*
      var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

      if (month.length < 2) 
          month = '0' + month;
      if (day.length < 2) 
          day = '0' + day;

      var currentdate = year+month+day
      */
      
      c.download = "Copy of Ports Used for "+asaname+".txt";

      
      
      var t = new Blob([data], {
      type: "text/plain"
      });
      c.href = window.URL.createObjectURL(t);
      c.click();
    }

/*
function showincolor() {
  var table = document.getElementById('mytable');   

  var rows = mytable.getElementsByTagName("tr"); 

  for(i = 0; i < rows.length; i++){           

//manipulate rows 

    if(i % 2 == 0){ 

      rows[i].className = "even"; 

    }else{ 

      rows[i].className = "odd"; 

    }       


}}
*/
  /*
function showincolor(){
  var datarow2 = document.getElementById("datarow").innerHTML;
  console.log('Right before printing of data row')
  console.log(datarow2)
  if (datarow2.includes("Yes")){
    console.log('Inside of Yes if statment')
    
    document.getElementById("datarow").style.backgroundColor = 'red';

  }
  if (datarow2.includes('No')){
    document.getElementById("datarow").style.backgroundColor = 'green';
    

  }}*/
</script>

</body>
</html>
