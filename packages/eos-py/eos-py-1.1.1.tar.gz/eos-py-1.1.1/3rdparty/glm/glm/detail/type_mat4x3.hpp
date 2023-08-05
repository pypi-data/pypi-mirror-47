/// @ref core
/// @file glm/detail/type_mat4x3.hpp

#pragma once

#include "../fwd.hpp"
#include "type_vec3.hpp"
#include "type_vec4.hpp"
#include "type_mat.hpp"
#include <limits>
#include <cstddef>

namespace glm
{
	template <typename T, precision P = defaultp>
	struct tmat4x3
	{
		typedef tvec3<T, P> col_type;
		typedef tvec4<T, P> row_type;
		typedef tmat4x3<T, P> type;
		typedef tmat3x4<T, P> transpose_type;
		typedef T value_type;

	private:
		col_type value[4];

	public:
		// -- Constructors --

		GLM_FUNC_DECL tmat4x3() GLM_DEFAULT_CTOR;
		GLM_FUNC_DECL tmat4x3(tmat4x3<T, P> const & m) GLM_DEFAULT;
		template <precision Q>
		GLM_FUNC_DECL tmat4x3(tmat4x3<T, Q> const & m);

		GLM_FUNC_DECL GLM_CONSTEXPR_CTOR explicit tmat4x3(ctor);
		GLM_FUNC_DECL explicit tmat4x3(T const & x);
		GLM_FUNC_DECL tmat4x3(
			T const & x0, T const & y0, T const & z0,
			T const & x1, T const & y1, T const & z1,
			T const & x2, T const & y2, T const & z2,
			T const & x3, T const & y3, T const & z3);
		GLM_FUNC_DECL tmat4x3(
			col_type const & v0,
			col_type const & v1,
			col_type const & v2,
			col_type const & v3);

		// -- Conversions --

		template <
			typename X1, typename Y1, typename Z1,
			typename X2, typename Y2, typename Z2,
			typename X3, typename Y3, typename Z3,
			typename X4, typename Y4, typename Z4>
		GLM_FUNC_DECL tmat4x3(
			X1 const & x1, Y1 const & y1, Z1 const & z1,
			X2 const & x2, Y2 const & y2, Z2 const & z2,
			X3 const & x3, Y3 const & y3, Z3 const & z3,
			X4 const & x4, Y4 const & y4, Z4 const & z4);

		template <typename V1, typename V2, typename V3, typename V4>
		GLM_FUNC_DECL tmat4x3(
			tvec3<V1, P> const & v1,
			tvec3<V2, P> const & v2,
			tvec3<V3, P> const & v3,
			tvec3<V4, P> const & v4);

		// -- Matrix conversions --

		template <typename U, precision Q>
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat4x3<U, Q> const & m);

		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat2x2<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat3x3<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat4x4<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat2x3<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat3x2<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat2x4<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat4x2<T, P> const & x);
		GLM_FUNC_DECL GLM_EXPLICIT tmat4x3(tmat3x4<T, P> const & x);

		// -- Accesses --

		typedef length_t length_type;
		GLM_FUNC_DECL static length_type length(){return 4;}

		GLM_FUNC_DECL col_type & operator[](length_type i);
		GLM_FUNC_DECL col_type const & operator[](length_type i) const;

		// -- Unary arithmetic operators --

		GLM_FUNC_DECL tmat4x3<T, P> & operator=(tmat4x3<T, P> const & m) GLM_DEFAULT;

		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator=(tmat4x3<U, P> const & m);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator+=(U s);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator+=(tmat4x3<U, P> const & m);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator-=(U s);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator-=(tmat4x3<U, P> const & m);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator*=(U s);
		template <typename U>
		GLM_FUNC_DECL tmat4x3<T, P> & operator/=(U s);

		// -- Increment and decrement operators --

		GLM_FUNC_DECL tmat4x3<T, P> & operator++();
		GLM_FUNC_DECL tmat4x3<T, P> & operator--();
		GLM_FUNC_DECL tmat4x3<T, P> operator++(int);
		GLM_FUNC_DECL tmat4x3<T, P> operator--(int);
	};

	// -- Unary operators --

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator+(tmat4x3<T, P> const & m);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator-(tmat4x3<T, P> const & m);

	// -- Binary operators --

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator+(tmat4x3<T, P> const & m, T const & s);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator+(tmat4x3<T, P> const & m1, tmat4x3<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator-(tmat4x3<T, P> const & m, T const & s);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator-(tmat4x3<T, P> const & m1, tmat4x3<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator*(tmat4x3<T, P> const & m, T const & s);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator*(T const & s, tmat4x3<T, P> const & m);

	template <typename T, precision P>
	GLM_FUNC_DECL typename tmat4x3<T, P>::col_type operator*(tmat4x3<T, P> const & m, typename tmat4x3<T, P>::row_type const & v);

	template <typename T, precision P>
	GLM_FUNC_DECL typename tmat4x3<T, P>::row_type operator*(typename tmat4x3<T, P>::col_type const & v, tmat4x3<T, P> const & m);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat2x3<T, P> operator*(tmat4x3<T, P> const & m1, tmat2x4<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat3x3<T, P> operator*(tmat4x3<T, P> const & m1,	tmat3x4<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator*(tmat4x3<T, P> const & m1, tmat4x4<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator/(tmat4x3<T, P> const & m, T const & s);

	template <typename T, precision P>
	GLM_FUNC_DECL tmat4x3<T, P> operator/(T const & s, tmat4x3<T, P> const & m);

	// -- Boolean operators --

	template <typename T, precision P>
	GLM_FUNC_DECL bool operator==(tmat4x3<T, P> const & m1, tmat4x3<T, P> const & m2);

	template <typename T, precision P>
	GLM_FUNC_DECL bool operator!=(tmat4x3<T, P> const & m1, tmat4x3<T, P> const & m2);
}//namespace glm

#ifndef GLM_EXTERNAL_TEMPLATE
#include "type_mat4x3.inl"
#endif //GLM_EXTERNAL_TEMPLATE
