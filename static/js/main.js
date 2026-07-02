const counters = document.querySelectorAll(".counter");

const speed = 200;

counters.forEach(counter => {

    const update = () => {

        const target = +counter.dataset.target;

        const count = +counter.innerText;

        const increment = target / speed;

        if(count < target){

            counter.innerText = Math.ceil(count + increment);

            setTimeout(update,10);

        }else{

            counter.innerText = target;

        }

    }

    update();

});