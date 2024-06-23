use std::collections::HashMap;

use pyo3::{
    exceptions::PyTypeError, pyclass, pymethods, FromPyObject, IntoPy, Py, PyAny, PyResult, Python,
};

#[derive(Clone)]
pub enum AttrValue {
    String(String),
    Integer(i64),
    Float(f64),
    Boolean(bool),
    Classes(Vec<String>),
    Styles(HashMap<String, String>),
}

impl AttrValue {
    fn to_html(&self) -> String {
        match self {
            Self::String(value) => value.clone(),
            Self::Integer(number) => number.to_string(),
            Self::Float(number) => number.to_string(),
            Self::Boolean(value) => {
                if *value {
                    value.to_string()
                } else {
                    String::new()
                }
            }
            Self::Classes(values) => values.join(" "),
            Self::Styles(mapping) => mapping
                .iter()
                .map(|(key, value)| format!("{key}:{value}"))
                .collect::<Vec<String>>()
                .join(";"),
        }
    }
}

impl<'py> FromPyObject<'py> for AttrValue {
    fn extract(ob: &'py PyAny) -> PyResult<Self> {
        if let Ok(data) = ob.extract::<String>() {
            Ok(Self::String(data))
        } else if let Ok(data) = ob.extract::<i64>() {
            Ok(Self::Integer(data))
        } else if let Ok(data) = ob.extract::<f64>() {
            Ok(Self::Float(data))
        } else if let Ok(data) = ob.extract::<bool>() {
            Ok(Self::Boolean(data))
        } else if let Ok(data) = ob.extract::<Vec<String>>() {
            Ok(Self::Classes(data))
        } else if let Ok(data) = ob.extract::<HashMap<String, String>>() {
            Ok(Self::Styles(data))
        } else {
            return Err(PyTypeError::new_err("Unknown type".to_string()));
        }
    }
}

impl IntoPy<Py<PyAny>> for AttrValue {
    fn into_py(self, py: Python<'_>) -> Py<PyAny> {
        match self {
            Self::String(value) => value.into_py(py),
            Self::Integer(number) => number.into_py(py),
            Self::Float(number) => number.into_py(py),
            Self::Boolean(value) => value.into_py(py),
            Self::Classes(values) => values.into_py(py),
            Self::Styles(items) => items.into_py(py),
        }
    }
}

#[derive(Clone, Default)]
pub struct Attrs {
    values: HashMap<String, AttrValue>,
}

impl Attrs {
    fn is_empty(&self) -> bool {
        self.values.is_empty()
    }

    fn to_html(&self) -> String {
        self.values
            .iter()
            .filter_map(|(key, attr_value)| {
                let value = attr_value.to_html();
                if value.is_empty() {
                    None
                } else {
                    Some(format!("{key}=\"{value}\""))
                }
            })
            .collect::<Vec<String>>()
            .join(" ")
    }
}

impl<'py> FromPyObject<'py> for Attrs {
    fn extract(ob: &'py PyAny) -> PyResult<Self> {
        Ok(Attrs {
            values: ob.extract::<HashMap<String, AttrValue>>()?,
        })
    }
}

impl IntoPy<Py<PyAny>> for Attrs {
    fn into_py(self, py: Python<'_>) -> Py<PyAny> {
        self.values.into_py(py)
    }
}

#[derive(Clone)]
pub enum Child {
    Unsafe(String),
    Safe(String),
    Integer(i64),
    Float(f64),
    Boolean(bool),
    Element(BaseElement),
    Component(Py<PyAny>),
}

impl Child {
    fn add_context(&mut self, context: &HashMap<String, Py<PyAny>>) -> PyResult<()> {
        if context.is_empty() {
            return Ok(());
        }
        match self {
            Self::Element(element) => {
                for child in element.children.iter_mut() {
                    child.add_context(context)?;
                }
            }
            Self::Component(component) => {
                let mut err = None;
                Python::with_gil(|py| {
                    let Ok(component_context) = component.getattr(py, "context") else {
                        err = Some(PyTypeError::new_err(
                            "Object has no attribute context".to_string(),
                        ));
                        return;
                    };
                    let Ok(_) = component_context.call_method1(py, "update", (context.clone(),))
                    else {
                        err = Some(PyTypeError::new_err(
                            "Object context has no method update".to_string(),
                        ));
                        return;
                    };
                });
                if let Some(error) = err {
                    return Err(error);
                }
            }
            _ => (),
        }
        Ok(())
    }

    fn to_html(&mut self) -> PyResult<String> {
        match self {
            Self::Unsafe(value) => Ok(value.clone()),
            Self::Safe(value) => Ok(value.clone()),
            Self::Integer(number) => Ok(number.to_string()),
            Self::Float(number) => Ok(number.to_string()),
            Self::Boolean(value) => Ok(value.to_string()),
            Self::Element(element) => Ok(element.to_html()?),
            Self::Component(component) => {
                Python::with_gil(|py| component.call_method0(py, "render")?.extract::<String>(py))
            }
        }
    }
}

impl<'py> FromPyObject<'py> for Child {
    fn extract(ob: &'py PyAny) -> PyResult<Self> {
        if let Ok(value) = ob.extract::<String>() {
            Ok(Child::Unsafe(value))
        } else if let Ok(number) = ob.extract::<i64>() {
            Ok(Child::Integer(number))
        } else if let Ok(number) = ob.extract::<f64>() {
            Ok(Child::Float(number))
        } else if let Ok(value) = ob.extract::<bool>() {
            Ok(Child::Boolean(value))
        } else if let Ok(element) = ob.extract::<BaseElement>() {
            Ok(Child::Element(element))
        } else {
            Python::with_gil(|py| Ok(Child::Component(ob.into_py(py))))
        }
    }
}

impl IntoPy<Py<PyAny>> for Child {
    #[inline]
    fn into_py(self, py: Python<'_>) -> Py<PyAny> {
        match self {
            Self::Unsafe(value) => value.into_py(py),
            Self::Safe(value) => value.into_py(py),
            Self::Integer(number) => number.into_py(py),
            Self::Float(number) => number.into_py(py),
            Self::Boolean(value) => value.into_py(py),
            Self::Element(element) => element.into_py(py),
            Self::Component(component) => component,
        }
    }
}

/// Class representing an HTML element
#[pyclass(subclass)]
#[derive(Clone)]
pub struct BaseElement {
    #[pyo3(get)]
    pub html_name: &'static str,
    #[pyo3(get)]
    pub html_header: Option<&'static str>,
    #[pyo3(get)]
    pub void_element: bool,

    #[pyo3(get)]
    pub children: Vec<Child>,
    #[pyo3(get)]
    pub attrs: Attrs,
    #[pyo3(get)]
    pub context: HashMap<String, Py<PyAny>>,
}

#[pymethods]
impl BaseElement {
    pub fn __len__(&self) -> usize {
        self.children.len()
    }

    pub fn __repr__(&self) -> String {
        let mut tag = format!("<{}", self.html_name);

        if self.has_attributes() {
            tag.push(' ');
            tag.push_str(&self.attrs.to_html());
        }

        tag.push('>');

        if !self.void_element {
            if !self.children.is_empty() {
                tag.push_str("...");
            }
            tag.push_str(&format!("</{}>", self.html_name));
        }

        tag
    }

    pub fn __str__(&mut self) -> PyResult<String> {
        return self.to_html()
    }

    pub fn is_simple(&self) -> bool {
        self.children.len() == 1
            && self
                .children
                .iter()
                .all(|child| !matches!(child, Child::Element(_)))
    }

    pub fn has_attributes(&self) -> bool {
        !self.attrs.is_empty()
    }

    pub fn to_html(&mut self) -> PyResult<String> {
        let mut tag = String::new();

        // HTML header
        if let Some(header) = self.html_header {
            tag.push_str(header);
            tag.push('\n');
        }

        // Opening tag
        tag.push('<');
        tag.push_str(self.html_name);

        // HTML element's attributes
        if self.has_attributes() {
            tag.push(' ');
            tag.push_str(&self.attrs.to_html());
        }

        // HTML element's children
        tag.push('>');
        if !self.void_element {
            for child in self.children.iter_mut() {
                child.add_context(&self.context)?;
                tag.push_str(&child.to_html()?);
            }

            // Closing tag
            tag.push_str(&format!("</{}>", self.html_name));
        }

        Ok(tag)
    }
}
