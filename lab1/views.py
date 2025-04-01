from django.shortcuts import render
from .cipher import SinglePermutationCipher, RoutePermutationCipher, MultilevelCipher


# Create your views here.
def index(request):
    return render(request, "index.html")


def lab1(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        cipher = SinglePermutationCipher()
        if form_type == "encrypt_form":
            message = request.POST.get("message", "")
            encrypted_message, encryption_key = cipher.encrypt(message)

            # Add both original and processed messages to context
            context["original_message"] = message
            context["encrypted_message"] = encrypted_message
            context["encryption_key"] = encryption_key

            return render(request, "lab1.html", context)
        elif form_type == "decrypt_form":
            encrypted_message = request.POST.get("encrypted_message", "")
            encryption_key = request.POST.get("encryption_key", "")
            decrypted_message = cipher.decrypt(encrypted_message, encryption_key)

            # Add both original and processed messages to context
            context["decrypted_message"] = decrypted_message

            return render(request, "lab1.html", context)
        elif form_type == "route_encrypt_form":
            message = request.POST.get("route_message", "")
            encrypted_message, key = RoutePermutationCipher().encrypt(message)

            # Add both original and processed messages to context
            context["route_original_message"] = message
            context["route_encrypted_message"] = encrypted_message
            context["route_encryption_key"] = key

            return render(request, "lab1.html", context)
        elif form_type == "route_decrypt_form":
            encrypted_message = request.POST.get("route_encrypted_message", "")
            encryption_key = request.POST.get("route_encryption_key", "")
            decrypted_message = RoutePermutationCipher().decrypt(encrypted_message, encryption_key)

            # Add both original and processed messages to context
            context["route_decrypted_message"] = decrypted_message

            return render(request, "lab1.html", context)
        elif form_type == "multilevel_encrypt_form":
            message = request.POST.get("multilevel_message", "")
            encrypted_message, encryption_key = MultilevelCipher().encrypt(message)

            # Add both original and processed messages to context
            context["multilevel_original_message"] = message
            context["multilevel_encrypted_message"] = encrypted_message
            context["multilevel_encryption_key"] = encryption_key

            return render(request, "lab1.html", context)
        elif form_type == "multilevel_decrypt_form":
            encrypted_message = request.POST.get("multilevel_encrypted_message", "")
            encryption_key = request.POST.get("multilevel_encryption_key", "")
            decrypted_message = MultilevelCipher().decrypt(
                encrypted_message, encryption_key
            )

            # Add both original and processed messages to context
            context["multilevel_decrypted_message"] = decrypted_message

            return render(request, "lab1.html", context)
    else:
        context["original_message"] = ""
        context["encrypted_message"] = ""
        context["encryption_key"] = ""

        return render(request, "lab1.html", context)
