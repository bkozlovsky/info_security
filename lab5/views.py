import ast
from django.shortcuts import render
from .cipher import RSACipher


# Create your views here.
def lab5(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "rsa_encrypt_form":
            message = request.POST.get("rsa_original_message", "")

            encrypted_message, public_key = RSACipher().encrypt(message)

            # Add both original and processed messages to context
            context["rsa_original_message"] = message
            context["rsa_public_key"] = public_key
            context["rsa_encrypted_message"] = encrypted_message

            return render(request, "lab5.html", context)
        elif form_type == "rsa_decrypt_form":
            encrypted_message = request.POST.get("rsa_encrypted_message", "")
            public_key = request.POST.get("rsa_public_key", "")

            decrypted_message = RSACipher().decrypt(ast.literal_eval(encrypted_message), ast.literal_eval(public_key))

            context["rsa_decrypted_message"] = decrypted_message

            return render(request, "lab5.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab5.html", context)
