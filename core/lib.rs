use std::collections::HashMap;

use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

// #[pyclass]
// struct BaseElement {
//     #[pyo3(get)]
//     children: Py<PyTuple>,
//     #[pyo3(get)]
//     attrs: Py<PyDict>,
//     #[pyo3(get)]
//     context: Py<PyDict>,
// }

// #[pymethods]
// impl BaseElement {
//     #[new]
//     #[pyo3(signature = (*children, **attrs))]
//     fn new<'py>(children: &Bound<'_, PyTuple>, attrs: Option<&Bound<'_, PyDict>>) -> Self {
//         Python::with_gil(|py| {
//             BaseElement {
//                 children: children.into_py(py),
//                 attrs: attrs.map_or(PyDict::new_bound(py), |dict| dict.clone()).unbind(),
//                 context: PyDict::new_bound(py).unbind(),
//             }
//         })
//     }

//     fn __str__(&self) -> String {
//         self.to_string(true)
//     }

//     fn __repr__(&self) -> String {
//         self.to_string(false)
//     }

//     fn __len__(&self) -> usize {
//         Python::with_gil(|py| {
//             self.children.into_bound(py).len()
//         })
//     }

//     fn __iter__(&self) -> BoundTupleIterator<'_> {
//         Python::with_gil(|py| {
//             self.children.into_bound(py).into_iter()
//         })
//     }

//     fn is_simple(&self) -> bool {
//         Python::with_gil(|py| {
//             let children = self.children.into_bound(py);
//             children.len() == 1
//         })
//     }

//     fn has_attributes(&self) -> bool {
//         Python::with_gil(|py| {
//             !self.attrs.into_bound(py).is_empty()
//         })
//     }

//     fn to_html(&self) -> String {
//         Python::with_gil(|py| {
//             let mut dom = self;
//             let mut classes = self
//         })
//     }
// }

#[pyfunction]
fn to_html(obj: &Bound<'_, PyAny>) -> PyResult<String> {
    let mut dom = obj.clone();
    let classes = obj.getattr("classes")?;

    loop {
        let rendered_dom = dom.call_method0("render")?;

        if (dom.as_ptr() as isize) == (rendered_dom.as_ptr() as isize) {
            break;
        }

        let context = rendered_dom.getattr("context")?;
        dom = rendered_dom;

        context.call_method1("update", (dom.getattr("context")?,))?;
        classes.call_method1("extend", (dom.getattr("classes")?,))?;
    }

    let mut element_tag = String::new();
    if let Ok(header) = dom.getattr("html_header")?.extract::<String>() {
        element_tag.push_str(&format!("{header}\n"));
    }

    let children_str: String = dom.call_method0("_format_children")?.extract()?;
    let html_name: String = dom.getattr("html_name")?.extract()?;

    if html_name == "__hidden__" {
        return Ok(children_str);
    }

    element_tag.push_str(&format!("<{html_name}"));
    let has_attributes: bool = dom.call_method0("has_attributes")?.extract()?;

    if has_attributes || classes.call_method0("__len__")?.extract::<usize>()? > 0 {
        let attrs_str = dom
            .call_method1("_format_attributes", (classes, true))?
            .extract::<String>()?;

        element_tag.push(' ');
        element_tag.push_str(&attrs_str);
    }

    if children_str.is_empty() && dom.getattr("void_element")?.extract::<bool>()? {
        element_tag.push('>');
    } else {
        element_tag.push_str(&format!(">{children_str}</{html_name}>"));
    }

    Ok(element_tag)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn ludicrous(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(to_html, m)?)?;
    Ok(())
}
