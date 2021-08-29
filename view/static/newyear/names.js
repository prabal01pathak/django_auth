let counter = 0;
let tags = document.querySelector('p');

function count() {
	if(counter%10==0 && counter !=0){
		alert(`You have clicked ${counter} times`);
	}
	counter++;
	tags.innerHTML=counter;
	return counter
}
document.querySelector('button').onclick=count;
function change(){
	counting = count();
	string=`Second Page and counter is ${counting}`;
	document.querySelector('div').innerHTMl = string;
	alert(counting);
	
}



document.addEventListener('DOMContentLoaded',
	function() {
		document.querySelector('form').onsubmit = 
		function() {
			let name =document.querySelector('#name').value;
			alert(`Hello ${name}`);
		}
	}
)

