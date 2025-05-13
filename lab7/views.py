import ast
from django.shortcuts import render
from .cipher import ElGamalCipher


# Create your views here.
def lab7(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "elgamal_encrypt_form":
            message = request.POST.get("elgamal_original_message", "")

            encrypted_message, public_key = ElGamalCipher().encrypt(message)

            # Add both original and processed messages to context
            context["elgamal_original_message"] = message
            context["elgamal_public_key"] = public_key
            context["elgamal_encrypted_message"] = encrypted_message

            return render(request, "lab7.html", context)
        elif form_type == "elgamal_decrypt_form":
            encrypted_message = request.POST.get("elgamal_encrypted_message", "")
            public_key = request.POST.get("elgamal_public_key", "")

            decrypted_message = ElGamalCipher().decrypt(ast.literal_eval(encrypted_message), ast.literal_eval(public_key))

            context["elgamal_decrypted_message"] = decrypted_message

            return render(request, "lab7.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab7.html", context)
