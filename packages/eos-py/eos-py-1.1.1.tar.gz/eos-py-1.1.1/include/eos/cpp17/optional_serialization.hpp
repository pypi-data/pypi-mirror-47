/*
 * eos - A 3D Morphable Model fitting library written in modern C++11/14.
 *
 * File: include/eos/cpp17/optional_serialization.hpp
 *
 * Copyright 2018 Patrik Huber
 *
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
 */
#pragma once

#ifndef EOS_OPTIONAL_SERIALIZATION_HPP_
#define EOS_OPTIONAL_SERIALIZATION_HPP_

#if __cplusplus >= 201703L || (defined(_MSVC_LANG) && _MSVC_LANG >= 201703L)
  #include "cereal/types/optional.hpp"
#else
  #include "eos/cpp17/detail/akrzemi1_optional_serialization.hpp"
#endif

#endif /* EOS_OPTIONAL_SERIALIZATION_HPP_ */
