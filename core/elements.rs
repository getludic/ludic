#![allow(non_camel_case_types)]

use pyo3::{Py, PyAny, pyclass, pymethods};
use std::collections::HashMap;

use crate::base::{Attrs, BaseElement, Child};

#[pyclass(extends=BaseElement, subclass)]
pub struct style;

#[pymethods]
impl style {
    #[new]
    #[pyo3(signature = (styles, theme=None, **attrs))]
    pub fn new(styles: Child, theme: Option<Py<PyAny>>, attrs: Option<Attrs>) -> (Self, BaseElement) {
        let mut context = HashMap::new();
        if let Some(value) = theme {
            context.insert("theme".to_string(), value);
        }

        (
            Self,
            BaseElement {
                html_name: "style",
                html_header: None,
                void_element: false,
                children: vec![styles],
                attrs: attrs.unwrap_or_default(),
                context,
            },
        )
    }
}

#[pyclass(name="output", extends=BaseElement, subclass)]
pub struct output_;

#[pymethods]
impl output_ {
    #[new]
    #[pyo3(signature = (*children, **attrs))]
    pub fn new(children: Vec<Child>, attrs: Option<Attrs>) -> (Self, BaseElement) {
        (
            Self,
            BaseElement {
                html_name: "output",
                html_header: None,
                void_element: false,
                children,
                attrs: attrs.unwrap_or_default(),
                context: HashMap::new(),
            },
        )
    }
}

macro_rules! element {
    ($name:ident, $header:expr, $void:expr) => {
        #[pyclass(extends=BaseElement, subclass)]
        pub struct $name;

        #[pymethods]
        impl $name {
            #[new]
            #[pyo3(signature = (*children, **attrs))]
            pub fn new(children: Vec<Child>, attrs: Option<Attrs>) -> (Self, BaseElement) {
                (
                    Self,
                    BaseElement {
                        html_name: stringify!($name),
                        html_header: $header,
                        void_element: $void,
                        children,
                        attrs: attrs.unwrap_or_default(),
                        context: HashMap::new(),
                    },
                )
            }
        }
    };
}

element!(div, None, false);
element!(span, None, false);
element!(main, None, false);
element!(p, None, false);
element!(a, None, false);
element!(br, None, true);
element!(button, None, false);
element!(label, None, false);
element!(td, None, false);
element!(th, None, false);
element!(tr, None, false);
element!(thead, None, false);
element!(tbody, None, false);
element!(tfoot, None, false);
element!(table, None, false);
element!(li, None, false);
element!(ul, None, false);
element!(ol, None, false);
element!(dt, None, false);
element!(dd, None, false);
element!(dl, None, false);
element!(section, None, false);
element!(input, None, true);
element!(legend, None, false);
element!(option, None, false);
element!(optgroup, None, false);
element!(select, None, false);
element!(textarea, None, false);
element!(fieldset, None, false);
element!(form, None, false);
element!(img, None, true);
element!(svg, None, false);
element!(circle, None, false);
element!(line, None, false);
element!(path, None, false);
element!(polyline, None, false);
element!(b, None, false);
element!(i, None, false);
element!(s, None, false);
element!(u, None, false);
element!(strong, None, false);
element!(em, None, false);
element!(mark, None, false);
element!(del_, None, false);
element!(ins, None, false);
element!(header, None, false);
element!(big, None, false);
element!(small, None, false);
element!(code, None, false);
element!(pre, None, false);
element!(cite, None, false);
element!(blockquote, None, false);
element!(abbr, None, false);
element!(h1, None, false);
element!(h2, None, false);
element!(h3, None, false);
element!(h4, None, false);
element!(h5, None, false);
element!(h6, None, false);
element!(title, None, false);
element!(link, None, true);
element!(script, None, false);
element!(noscript, None, false);
element!(meta, None, true);
element!(head, None, false);
element!(body, None, false);
element!(footer, None, false);
element!(html, Some("<!doctype html>"), false);
element!(iframe, None, false);
element!(article, None, false);
element!(address, None, false);
element!(caption, None, false);
element!(col, None, true);
element!(colgroup, None, false);
element!(area, None, true);
element!(aside, None, false);
element!(source, None, true);
element!(audio, None, false);
element!(base, None, true);
element!(bdi, None, false);
element!(bdo, None, false);
element!(canvas, None, false);
element!(data, None, false);
element!(datalist, None, false);
element!(details, None, false);
element!(dfn, None, false);
element!(dialog, None, false);
element!(embed, None, true);
element!(figcaption, None, false);
element!(figure, None, false);
element!(hrgroup, None, false);
element!(hr, None, true);
element!(kbd, None, false);
element!(map, None, false);
element!(menu, None, false);
element!(meter, None, false);
element!(nav, None, false);
element!(object, None, false);
element!(param, None, true);
element!(picture, None, false);
element!(progress, None, false);
element!(q, None, false);
element!(rp, None, false);
element!(rt, None, false);
element!(ruby, None, false);
element!(samp, None, false);
element!(search, None, false);
element!(sub, None, false);
element!(summary, None, false);
element!(sup, None, false);
element!(template, None, false);
element!(time, None, false);
element!(track, None, true);
element!(var, None, false);
element!(video, None, false);
element!(wbr, None, true);
