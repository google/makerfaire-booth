import * as tfc from '@tensorflow/tfjs-core';
import {BurgerNet} from './burgernet';
import imageURL from './burger_000156.png';

const burger = document.getElementById('burger');
burger.onload = async () => {
    const resultElement = document.getElementById('result');

    resultElement.innerText = 'Loading Burgernet...';

    const burgernet = new BurgerNet();
    console.time('Loading of model');
    await burgernet.load();
    console.timeEnd('Loading of model');

    const pixels = tfc.fromPixels(burger);

    let result = burgernet.predict(pixels);
    console.log("result: ", result);
    burgernet.dispose();
};
burger.src = imageURL;
