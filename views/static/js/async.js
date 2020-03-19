function pairs() {
    $.ajax({
	    url: '/pairs',
	    success: function(){
	    console.log("Graph draw started");
	    	//alert("ok");
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}


function pair(name) {
    $.ajax({
	    url: '/pair?entity='+name,
	    success: function(data){
	    console.log("Graph draw started");
	    	//alert("ok");
	    },
	    error: function(error){
		    console.log(error);
	    }
    });
}
