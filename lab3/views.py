from django.shortcuts import render
from .cipher import AdditiveCipher, ModAdditionCipher

# Create your views here.


def lab3(request):
    context = {}

    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "modaddition_encrypt_form":
            message = request.POST.get("modaddition_original_message", "")
            key = request.POST.get("modaddition_encryption_key", "")
            encrypted_message = ModAdditionCipher().encrypt(message, key)

            # Add both original and processed messages to context
            context["modaddition_original_message"] = message
            context["modaddition_encrypted_message"] = encrypted_message
            context["modaddition_encryption_key"] = key

            return render(request, "lab3.html", context)
        elif form_type == "modaddition_decrypt_form":
            encrypted_message = request.POST.get("modaddition_encrypted_message", "")
            encryption_key = request.POST.get("modaddition_encryption_key", "")
            decrypted_message, table_data = ModAdditionCipher().decrypt(
                encrypted_message, encryption_key
            )

            # Split by '|', strip whitespace, remove empty strings
            cells = [
                cell.strip()
                for cell in table_data.strip().split("|")
                if cell.strip() != ""
            ]

            # Group cells into rows
            row_length = len(encrypted_message)
            decrypted_table = [
                cells[i : i + row_length] for i in range(0, len(cells), row_length)
            ]

            context["modaddition_decrypted_message"] = decrypted_message
            context["modaddition_decrypted_table"] = decrypted_table

            return render(request, "lab3.html", context)

        elif form_type == "additive_encrypt_form":
            message = request.POST.get("additive_original_message", "")
            encryption_data = AdditiveCipher().encrypt(message)

            # Add both original and processed messages to context
            context["additive_original_message"] = message
            context["additive_encrypted_message"] = encryption_data[0]

            return render(request, "lab3.html", context)
        elif form_type == "additive_decrypt_form":
            message = request.POST.get("additive_encrypted_message", "")
            key = request.POST.get("additive_encryption_key", "")
            decrypted_message = AdditiveCipher().decrypt(message, 34)

            context["additive_decrypted_message"] = decrypted_message

            return render(request, "lab3.html", context)
    else:
        context["original_message"] = ""
        context["encrypted_data"] = ""

        return render(request, "lab3.html", context)
