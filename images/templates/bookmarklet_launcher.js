(function(){
	console.log('hiiiii');
	if (window.bookmarklet !== undefined){
			console.log('if');
console.log(window.bookmarklet);
		bookmarklet();
	}
	else{
		console.log('else');


		document.body.appendChild(document.createElement('script')).src='https://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*9999999999999999);
	}
})();