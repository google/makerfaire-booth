/**
 * @license
 * Copyright 2017 Google Inc. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */

import {loadFrozenModel, NamedTensorMap} from '@tensorflow/tfjs-converter';
import * as tfc from '@tensorflow/tfjs-core';

const GOOGLE_CLOUD_STORAGE_DIR =
      'https://storage.googleapis.com/konerding-burgernet/';
const MODEL_FILE_URL = "tensorflowjs_model.pb";
const WEIGHT_MANIFEST_FILE_URL = 'weights_manifest.json';
const INPUT_NODE_NAME = 'input';
const OUTPUT_NODE_NAME = 'final_result';
const PREPROCESS_DIVISOR = tfc.scalar(255 / 2);

export class BurgerNet {
    constructor() {}

    async load() {
	this.model = await loadFrozenModel(
            GOOGLE_CLOUD_STORAGE_DIR + MODEL_FILE_URL,
            GOOGLE_CLOUD_STORAGE_DIR + WEIGHT_MANIFEST_FILE_URL);
    }

    dispose() {
	if (this.model) {
	    this.model.dispose();
	}
    }
    /**
     * Infer through BurgerNet. This does standard ImageNet pre-processing before
     * inferring through the model. This method returns named activations as well
     * as softmax logits.
     *
     * @param input un-preprocessed input Array.
     * @return The softmax logits.
     */
    predict(input) {
	const preprocessedInput = tfc.div(
            tfc.sub(input.asType('float32'), PREPROCESS_DIVISOR),
            PREPROCESS_DIVISOR);
	const reshapedInput =
              preprocessedInput.reshape([1, ...preprocessedInput.shape]);
	const dict = {};
	dict[INPUT_NODE_NAME] = reshapedInput;
	var result = this.model.execute(dict, OUTPUT_NODE_NAME);
	console.log("Result:", result);
	return result;
    }
}
