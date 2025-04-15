import ast
from django.shortcuts import render
from .cipher import PolybianSquare, HillCipher


# Create your views here.

def lab2(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "polybius_encrypt_form":
            message = request.POST.get("polybius_original_message", "")
            encrypted_message, encryption_key = PolybianSquare().encrypt(message)

            # Add both original and processed messages to context
            context["polybius_original_message"] = message
            context["polybius_encrypted_message"] = encrypted_message
            context["polybius_encryption_key"] = encryption_key
            context['range'] = range(1, len(encryption_key[0]) + 1)

            return render(request, "lab2.html", context)
        elif form_type == "polybius_decrypt_form":
            encrypted_message = request.POST.get("polybius_encrypted_message", "")
            encryption_key = request.POST.get("polybius_encryption_key", "")
            encryption_key = ast.literal_eval(encryption_key)
            decrypted_message = PolybianSquare().decrypt(encrypted_message, encryption_key)

            context["polybius_decrypted_message"] = decrypted_message

            return render(request, "lab2.html", context)
        elif form_type == "hill_encrypt_form":
            message = request.POST.get("hill_original_message", "")
            encrypted_data, encryption_matrix, decryption_matrix = HillCipher().encrypt(message)

            # Add both original and processed messages to context
            context["hill_original_message"] = message
            context["hill_encrypted_data"] = encrypted_data
            context["hill_encryption_matrix"] = encryption_matrix
            context["hill_decryption_matrix"] = decryption_matrix
            context['encryption_range'] = range(1, len(encryption_matrix[0]) + 1)
            context['decryption_range'] = range(1, len(decryption_matrix[0]) + 1)

            return render(request, "lab2.html", context)
        elif form_type == "hill_decrypt_form":
            encrypted_data = request.POST.get("hill_encrypted_data", "")
            decryption_matrix = request.POST.get("hill_decryption_matrix", "")
            encrypted_data = ast.literal_eval(encrypted_data)
            decryption_matrix = ast.literal_eval(decryption_matrix)
            decrypted_message = HillCipher().decrypt(encrypted_data, decryption_matrix)

            context["hill_decrypted_message"] = decrypted_message
            return render(request, "lab2.html", context)
    else:
        context["hill_original_message"] = ""
        context["hill_encrypted_data"] = ""
        context["hill_encryption_matrix"] = ""
        context["hill_decryption_matrix"] = ""
        context['encryption_range'] = ""
        context['decryption_range'] = ""

        return render(request, "lab2.html", context)
