.. _api_reference:

=============
API Reference
=============

Modules
=====================================

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   api.v1.cmd
   api.v1.data
   api.v1.auth
   util.v1.chroma_handler

cmd-Methods
------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   api.v1.cmd.cmd_ask_question

data-Methods
----------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   api.v1.data.data_add_texts
   api.v1.data.data_add_pdfs
   api.v1.data.data_get_texts
   api.v1.data.data_get_pdfs
   api.v1.data.data_get_databases
   api.v1.data.data_update_texts
   api.v1.data.data_delete_texts
   api.v1.data.data_delete_pdfs
   api.v1.data.data_delete_databases

auth-Methods
----------------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

#   util.v1.auth.fake_users_db
   util.v1.auth.verify_password
   util.v1.auth.get_password_hash
   util.v1.auth.get_user
   util.v1.auth.authenticate_user
   util.v1.auth.create_access_token
   util.v1.auth.get_current_user
   util.v1.auth.get_current_active_user

chroma_handler-Methods
------------------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   util.v1.chroma_handler.create_vector_store
   util.v1.chroma_handler.get_vector_store
   util.v1.chroma_handler.add_texts
   util.v1.chroma_handler.add_pdfs
   util.v1.chroma_handler.get_texts
   util.v1.chroma_handler.get_pdfs
   util.v1.chroma_handler.get_databases
   util.v1.chroma_handler.update_texts
   util.v1.chroma_handler.delete_texts
   util.v1.chroma_handler.delete_pdfs
   util.v1.chroma_handler.delete_databases
   util.v1.chroma_handler.build_question


Types
=====================================

Modules
------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   models.v1.cmd
   models.v1.data
   models.v1.auth

cmd-Models
-----------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   models.v1.cmd.RoleEnum
   models.v1.cmd.ChatAction
   models.v1.cmd.Question
   models.v1.cmd.CmdAskQuestionRequest
   models.v1.cmd.CmdAskQuestionResponse

data-Models
----------------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   models.v1.data.Text
   models.v1.data.TextUpdate
   models.v1.data.DataAddTextsRequest
   models.v1.data.DataAddTextsResponse
   models.v1.data.DataAddPDFsResponse
   models.v1.data.DataGetTextsRequest
   models.v1.data.DataGetTextsResponse
   models.v1.data.DataGetPDFsRequest
   models.v1.data.DataGetPDFsResponse
   models.v1.data.DataGetDatabasesResponse
   models.v1.data.DataUploadTextsRequest
   models.v1.data.DataUploadTextsResponse
   models.v1.data.DataDeleteTextsRequest
   models.v1.data.DataDeleteTextsResponse
   models.v1.data.DataDeletePDFsRequest
   models.v1.data.DataDeletePDFsResponse
   models.v1.data.DataDeleteDatabasesRequest
   models.v1.data.DataDeleteDatabasesResponse

auth-Models
------------------------------------

.. currentmodule:: fRAGme

.. autosummary::
   :nosignatures:
   :toctree: generated/
   :template: class.rst

   models.v1.auth.Token
   models.v1.auth.TokenData
   models.v1.auth.User
   models.v1.auth.UserInDB