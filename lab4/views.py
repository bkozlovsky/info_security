import ast
from django.shortcuts import render
from .cipher import LFSRCipher


# Create your views here.
def lab4(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "lsfr_encrypt_form":
            message = request.POST.get("lsfr_original_message", "")
            polynomial = request.POST.get("lsfr_polynomial", "")
            initial_state = request.POST.get("lsfr_initial_state", "")
            encrypted_message = LFSRCipher(
                ast.literal_eval(polynomial), ast.literal_eval(initial_state)
            ).encrypt(message)

            # Add both original and processed messages to context
            context["lsfr_original_message"] = message
            context["lsfr_encrypted_message"] = encrypted_message

            return render(request, "lab4.html", context)
        elif form_type == "lsfr_decrypt_form":
            encrypted_message = request.POST.get("lsfr_encrypted_message", "")
            polynomial = request.POST.get("lsfr_polynomial", "")
            initial_state = request.POST.get("lsfr_initial_state", "")
            decrypted_bytes = LFSRCipher(
                ast.literal_eval(polynomial), ast.literal_eval(initial_state)
            ).decrypt(ast.literal_eval(encrypted_message), return_bytes=True)
            decrypted_message = decrypted_bytes.decode("utf-8")

            context["lsfr_decrypted_message"] = decrypted_message
            context["lsfr_decrypted_bytes"] = decrypted_bytes

            return render(request, "lab4.html", context)

    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab4.html", context)
