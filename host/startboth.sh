#!/bin/bash
# Copyright 2016 Google
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Starts WhistleProxy _and_ WhistlePunk on the connected Android device, using adb:
# startboth.sh sensorId
#
# On launch, it will proxy the given sensorId, and bring up the WhistlePunk UI showing that id.
#
# Defaults to AccZ if no sensorId provided

sensorId=${1:-AccZ}
. startproxy.sh $sensorId
. startpunk.sh $sensorId
