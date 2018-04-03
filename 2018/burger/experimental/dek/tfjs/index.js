import * as tfc from '@tensorflow/tfjs-core';
import {MobileNet} from './mobilenet';
import imageURL from './cat.jpg';

const cat = document.getElementById('cat');
cat.onload = async () => {
    const resultElement = document.getElementById('result');

    resultElement.innerText = 'Loading MobileNet...';

    const mobileNet = new MobileNet();
    console.time('Loading of model');
    await mobileNet.load();
    console.timeEnd('Loading of model');

    const pixels = tfc.fromPixels(cat);

    console.time('First prediction');
    let result = mobileNet.predict(pixels);
    const topK = mobileNet.getTopKClasses(result, 5);
    console.timeEnd('First prediction');

    resultElement.innerText = '';
    topK.forEach(x => {
	resultElement.innerText += `${x.value.toFixed(3)}: ${x.label}\n`;
    });

    console.time('Subsequent predictions');
    result = mobileNet.predict(pixels);
    mobileNet.getTopKClasses(result, 5);
    console.timeEnd('Subsequent predictions');

    mobileNet.dispose();
};
cat.src = imageURL;
