import ast
from django.shortcuts import render
from .cipher import RSA_sign, ElGamal_sign


# Create your views here.
def lab9(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "rsa_sign_form":
            signatures = request.POST.get("rsa_signatures", "")
            signatures = ast.literal_eval(signatures)

            validation = []

            rsa = RSA_sign(n=77, e=7)
            for m, s in signatures:
                is_valid = rsa.verify(m, s)
                validation.append(is_valid)
            # Add both original and processed messages to context
            context["rsa_signatures"] = signatures
            context["rsa_validation"] = validation

            return render(request, "lab9.html", context)

        elif form_type == "elgamal_sign_form":
            elgamal_hash_message = request.POST.get("elgamal_hash_message", "")
            elgamal_hash_message = ast.literal_eval(elgamal_hash_message)
            el_gamal = ElGamal_sign(p=23, g=5, x=3)
            signature = el_gamal.sign(m=8, k=13)
            is_valid = el_gamal.verify(m=elgamal_hash_message, signature=signature)
            context["elgamal_signatures"] = signature
            context["elgamal_is_valid"] = is_valid
            return render(request, "lab9.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab9.html", context)
