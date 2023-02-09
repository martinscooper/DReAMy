
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForMaskedLM


def _extrac_CLS(sq, tokenizer, model, device="cpu", max_len=512, idx=0, layer=-1, truncate=True, padding=True):

    """""
    given a sequence, model (and tokenizer) extract the encoding for the sequnce
    idx 0 --> CLS
    idx 1 --> token 1
    idx 2 --> token 2
    .
    .
    .
    idx -1 --> SEP 
    """

    inputs = tokenizer(sq, truncation=truncate, padding=padding, return_tensors='pt')

    if device == "cuda":
        model.to(device)
        inputs.to(device)

    outputs = model(**inputs, output_hidden_states=True)
    last_hidden_states = outputs.hidden_states[layer]
    CLS = last_hidden_states[:,idx,:] # CLS = [0,0,:], 
    CLS = CLS.to("cpu").detach().numpy()

    if device == "cuda":
        model.to("cpu")
        inputs.to("cpu")

    return CLS

def get_encodings(list_of_dreams, model_name="bert-base-cased", device="cpu", max_len=512, idx=0, layer=-1, truncate=True):
    
    print("Loading/Downloading model and tokenizer")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)

    print("Collecting encodings")
    encodings = _extrac_CLS(
            list_of_dreams, tokenizer, model, 
            device=device, max_len=max_len, idx=idx, 
            layer=layer, truncate=truncate
            ) 

    return encodings
