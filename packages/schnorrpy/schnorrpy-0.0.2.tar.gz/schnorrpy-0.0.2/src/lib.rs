mod wrapper;
use wrapper::{__keypair_from_seed, __sign, __verify};

use pyo3::prelude::*;
use pyo3::{PyObject, FromPyObject, IntoPyObject};
use pyo3::types::{PyAny, PyBytes, PyTuple};

pub struct Seed([u8; 32]);
pub struct Keypair([u8; 32], [u8; 64]);
pub struct PublicKey([u8; 32]);
pub struct Signature([u8; 64]);
pub struct Message(Vec<u8>);

#[pymodule]
fn schnorrpy(_py: Python, m: &PyModule) -> PyResult<()> {
    /// Generate a key pair
    ///
    /// * seed: [u8] of size 32 containing the seed to generate the keypair
    ///
    /// Returned is a object, the first elment is the 32 byte public key,
    /// the second is the 64 byte private key
    #[pyfn(m, "keypair_from_seed")]
    pub fn keypair_from_seed(seed: Seed) -> PyResult<Keypair> {
        let keypair_arr = __keypair_from_seed(&seed.0);
        let mut private = [0u8; 64];
        let mut public = [0u8; 32];
        private.clone_from_slice(&keypair_arr[0..64]);
        public.clone_from_slice(&keypair_arr[64..96]);
        let keypair = Keypair(public, private);
        Ok(keypair)
    }

    /// Sign a message
    ///
    /// The combination of both public and private key must be provided
    /// This is effectively equivalent to a keypair.
    ///
    /// * keypair: Keypair used to sign the message
    /// * message: Vec<u8> containing the message to sign
    ///
    /// * returned object contains the signature consisting of 64 bytes.
    #[pyfn(m, "sign")]
    pub fn sign(keypair: Keypair, message: Message) -> PyResult<Signature> {
        let mut public = [0u8; 32];
        let mut private = [0u8; 64];
        public.clone_from_slice(&keypair.0[0..32]);
        private.clone_from_slice(&keypair.1[0..64]);
        let sig = __sign(&public, &private, &message.0);
        Ok(Signature(sig))
    }

    /// Verify a message and its corresponding against a public key
    ///
    /// * signature: [u8] of size 64, containing the signature to be verified
    /// * message: Vec<u8> containing the message to be verified
    /// * pubkey: [u8] of size 32 containing the public key used to verify the signature
    #[pyfn(m, "verify")]
    pub fn verify(signature: Signature, message: Message, pubkey: PublicKey) -> bool {
        __verify(&signature.0, &message.0, &pubkey.0)
    }

    Ok(())
}

// Convert Keypair struct to a PyTuple
impl IntoPyObject for Keypair {
    fn into_object(self, py: Python) -> PyObject {
        let secret = PyBytes::new(py, &self.0);
        let public = PyBytes::new(py, &self.1);
        PyTuple::new(py, vec![secret, public]).into_object(py)
    }
}

// Convert Signature struct to a PyObject
impl IntoPyObject for Signature {
    fn into_object(self, py: Python) -> PyObject {
        let sig = PyBytes::new(py, &self.0);
        sig.into_object(py)
    }
}

// Convert a PyTuple object to a Keypair struct
impl<'a> FromPyObject<'a> for Keypair {
    fn extract(obj: &'a PyAny) -> PyResult<Self> {
        let keypair = obj
            .downcast_ref::<PyTuple>()
            .expect("Expected a tuple");

        // Convert bytes to fixed width arrays
        let mut public: [u8; 32] = [0u8; 32];
        let mut private: [u8; 64] = [0u8; 64];
        public.clone_from_slice(
            &keypair.get_item(0)
                    .downcast_ref::<PyBytes>()
                    .expect("Expected a python Bytes object")
                    .as_bytes()[0..32]);
        private.clone_from_slice(
            &keypair.get_item(1)
                    .downcast_ref::<PyBytes>()
                    .expect("Expected a python Bytes object")
                    .as_bytes()[0..64]);
        let keypair = Keypair(public, private);
        Ok(keypair)
    }
}

// Convert a PyBytes object of size 32 to a Seed struct
impl<'a> FromPyObject<'a> for Seed {
    fn extract(obj: &'a PyAny) -> PyResult<Self> {
        let seed = obj
            .downcast_ref::<PyBytes>()
            .expect("Expected 32 byte seed");

        // Convert bytes to fixed width array
        let mut fixed: [u8; 32] = Default::default();
        fixed.clone_from_slice(seed.as_bytes());
        Ok(Seed(fixed))
    }
}

// Convert a PyBytes object of size 32 to a PublicKey struct
impl<'a> FromPyObject<'a> for PublicKey {
    fn extract(obj: &'a PyAny) -> PyResult<Self> {
        let pubkey = obj
            .downcast_ref::<PyBytes>()
            .expect("Expected 32 byte seed");

        // Convert bytes to fixed width array
        let mut fixed: [u8; 32] = Default::default();
        fixed.clone_from_slice(pubkey.as_bytes());
        Ok(PublicKey(fixed))
    }
}

// Convert a PyBytes object of size 64 to a Signature object
impl<'a> FromPyObject<'a> for Signature {
    fn extract(obj: &'a PyAny) -> PyResult<Self> {
        let signature = obj
            .downcast_ref::<PyBytes>()
            .expect("Expected 64 byte signature");

        // Convert bytes to fixed width array
        let mut fixed: [u8; 64] = [0u8; 64];
        fixed.clone_from_slice(signature.as_bytes());
        Ok(Signature(fixed))
    }
}

// Convert an arbitrary sized PyBytes object to a Message struct
impl<'a> FromPyObject<'a> for Message {
    fn extract(obj: &PyAny) -> PyResult<Self> {
        let messsge = obj
            .downcast_ref::<PyBytes>()
            .expect("Expected param to be an array of bytes");
        Ok(Message(messsge.as_bytes().to_owned()))
    }
}
