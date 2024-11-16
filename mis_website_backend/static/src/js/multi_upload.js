/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {ListController} from '@web/views/list/list_controller';
import {jsonrpc} from "@web/core/network/rpc_service";
import {AlertDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from '@web/core/l10n/translation';
patch(ListController.prototype, {
    //    /**
    //     * Handle the click event for upload documents.
    //     */
    _onClickAttachment: async function() {
        var self = this;
        const SelectedRecords = await self.getSelectedResIds()
        var OnSelectedDocument = function(e) {
            var result_doc = []
//            if (!file) return;
            for (var i = 0; i < this.files.length; i++) {
                (function(file) {

                    // Set desired max width and height and quality
                    const MAX_WIDTH = 800;
                    const MAX_HEIGHT = 800;
                    const QUALITY = 0.7;

                    // Read the file as a data URL
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = function(event) {
                        const img = new Image();
                        img.src = event.target.result;
                        img.onload = function() {
                            // Create a canvas element
                            const canvas = document.createElement("canvas");
                            let width = img.width;
                            let height = img.height;

                            // Resize if larger than max dimensions
                            if (width > height) {
                                if (width > MAX_WIDTH) {
                                    height *= MAX_WIDTH / width;
                                    width = MAX_WIDTH;
                                }
                            } else {
                                if (height > MAX_HEIGHT) {
                                    width *= MAX_HEIGHT / height;
                                    height = MAX_HEIGHT;
                                }
                            }

                            // Set canvas dimensions
                            canvas.width = width;
                            canvas.height = height;

                            // Draw the image on the canvas
                            const ctx = canvas.getContext("2d");
                            ctx.drawImage(img, 0, 0, width, height);

                            // Convert canvas to blob
                            canvas.toBlob(
                                function(blob) {
                                    // Upload or handle the compressed blob
                                    uploadCompressedImage(blob);
                                },
                                "image/jpeg",  // Image type
                                QUALITY        // Compression quality
                            );
                        };
                    };





                function uploadCompressedImage(blob) {
                    // You can use FormData to append the blob for upload
                    const formData = new FormData();
                    formData.append("image", blob, "compressed_image.jpg");

                    // Replace with your server upload logic
                    jsonrpc('/web/dataset/call_kw/upload.multi.documents/document_file_create', {
                            model: 'upload.multi.documents',
                            method: 'document_file_create',
                            args: [formData, file.name, SelectedRecords, self.props.resModel],
                            kwargs: {},
                        }).then(function(result) {
                            if (result) {
                                result_doc.push(result)
                            }
                        });
                }
            })
            }
            if (result_doc) {
                self.dialogService.add(AlertDialog, {
                    title: _t('Succeeded !!'),
                    body: _t("Updated successfully."),
                    confirmLabel: _t('Ok'),
                });
            } else {
                self.dialogService.add(AlertDialog, {
                    title: _t('Failed !!'),
                    body: _t("Please select record."),
                    confirmLabel: _t('Ok'),
                });
            }

        };
        var UploadFileDocument = $('<input type="file" multiple="multiple">');
        UploadFileDocument.click();
        UploadFileDocument.on('change', OnSelectedDocument);
    }
})
