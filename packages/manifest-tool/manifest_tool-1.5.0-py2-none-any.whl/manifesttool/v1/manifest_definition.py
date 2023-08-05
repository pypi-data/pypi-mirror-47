# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
#   The confidential and proprietary information contained in this file may
#   only be used by a person authorised under and to the extent permitted
#   by a subsisting licensing agreement from ARM Limited or its affiliates.
#
#          (C) COPYRIGHT 2016 ARM Limited or its affiliates.
#              ALL RIGHTS RESERVED
#
#   This entire notice must be reproduced on all copies of this file
#   and copies of this file may only be made by a person if such person is
#   permitted to do so under the terms of a subsisting license agreement
#   from ARM Limited or its affiliates.
#----------------------------------------------------------------------------
#
# This file has been generated using asn1ate (v <unknown>) from 'ASN.1/v1/manifest-1.0.0'
# Last Modified on 2019-03-18 12:08:08.480914
from pyasn1.type import univ, char, namedtype, namedval, tag, constraint, useful


class Uri(char.UTF8String):
    pass


class Bytes(univ.OctetString):
    pass


class UUID(univ.OctetString):
    pass


class Payload(univ.OctetString):
    pass


class CertificateReference(univ.Sequence):
    pass


CertificateReference.componentType = namedtype.NamedTypes(
    namedtype.NamedType('fingerprint', Bytes()),
    namedtype.NamedType('uri', Uri())
)


class SignatureBlock(univ.Sequence):
    pass


SignatureBlock.componentType = namedtype.NamedTypes(
    namedtype.NamedType('signature', univ.OctetString()),
    namedtype.NamedType('certificates', univ.SequenceOf(componentType=CertificateReference()))
)


class MacBlock(univ.Sequence):
    pass


MacBlock.componentType = namedtype.NamedTypes(
    namedtype.NamedType('pskID', univ.OctetString()),
    namedtype.NamedType('keyTableVersion', univ.Integer()),
    namedtype.OptionalNamedType('keyTableIV', univ.OctetString()),
    namedtype.OptionalNamedType('keyTableRef', char.UTF8String()),
    namedtype.NamedType('keyTableIndexSize', univ.Integer()),
    namedtype.NamedType('keyTableRecordSize', univ.Integer())
)


class KeyTableEntry(univ.Sequence):
    pass


KeyTableEntry.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('hash', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))),
    namedtype.OptionalNamedType('payloadKey', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))
)


class ResourceSignature(univ.Sequence):
    pass


ResourceSignature.componentType = namedtype.NamedTypes(
    namedtype.NamedType('hash', univ.OctetString()),
    namedtype.NamedType('signatures', univ.SequenceOf(componentType=SignatureBlock())),
    namedtype.OptionalNamedType('macs', univ.SequenceOf(componentType=MacBlock()))
)


class ResourceReference(univ.Sequence):
    pass


ResourceReference.componentType = namedtype.NamedTypes(
    namedtype.NamedType('hash', univ.OctetString()),
    namedtype.OptionalNamedType('uri', Uri()),
    namedtype.NamedType('size', univ.Integer())
)


class ResourceAlias(univ.Sequence):
    pass


ResourceAlias.componentType = namedtype.NamedTypes(
    namedtype.NamedType('hash', univ.OctetString()),
    namedtype.NamedType('uri', Uri())
)


class PayloadDescription(univ.Sequence):
    pass


PayloadDescription.componentType = namedtype.NamedTypes(
    namedtype.NamedType('format', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('enum', univ.Enumerated(namedValues=namedval.NamedValues(('undefined', 0), ('raw-binary', 1), ('cbor', 2), ('hex-location-length-data', 3), ('elf', 4), ('bsdiff-stream', 5)))),
        namedtype.NamedType('objectId', univ.ObjectIdentifier())
    ))
    ),
    namedtype.OptionalNamedType('encryptionInfo', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('initVector', univ.OctetString()),
        namedtype.NamedType('id', univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('key', univ.OctetString()),
            namedtype.NamedType('certificate', CertificateReference())
        ))
        ),
        namedtype.OptionalNamedType('key', univ.Choice(componentType=namedtype.NamedTypes(
            namedtype.NamedType('keyTable', Uri()),
            namedtype.NamedType('cipherKey', univ.OctetString())
        ))
        )
    ))
    ),
    namedtype.NamedType('storageIdentifier', char.UTF8String()),
    namedtype.NamedType('reference', ResourceReference()),
    namedtype.OptionalNamedType('installedSize', univ.Integer()),
    namedtype.OptionalNamedType('installedDigest', univ.OctetString()),
    namedtype.OptionalNamedType('version', char.UTF8String())
)


class Manifest(univ.Sequence):
    pass


Manifest.componentType = namedtype.NamedTypes(
    namedtype.NamedType('manifestVersion', univ.Enumerated(namedValues=namedval.NamedValues(('v1', 1)))),
    namedtype.OptionalNamedType('description', char.UTF8String()),
    namedtype.NamedType('timestamp', univ.Integer()),
    namedtype.NamedType('vendorId', UUID()),
    namedtype.NamedType('classId', UUID()),
    namedtype.NamedType('deviceId', UUID()),
    namedtype.NamedType('nonce', univ.OctetString()),
    namedtype.NamedType('vendorInfo', univ.OctetString()),
    namedtype.OptionalNamedType('precursorDigest', univ.OctetString()),
    namedtype.OptionalNamedType('applyPeriod', univ.Sequence(componentType=namedtype.NamedTypes(
        namedtype.NamedType('validFrom', univ.Integer()),
        namedtype.NamedType('validTo', univ.Integer())
    ))
    ),
    namedtype.NamedType('applyImmediately', univ.Boolean()),
    namedtype.OptionalNamedType('priority', univ.Integer()),
    namedtype.NamedType('encryptionMode', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('enum', univ.Enumerated(namedValues=namedval.NamedValues(('invalid', 0), ('aes-128-ctr-ecc-secp256r1-sha256', 1), ('none-ecc-secp256r1-sha256', 2), ('none-none-sha256', 3), ('none-psk-aes-128-ccm-sha256', 4), ('aes-128-ccm-psk-sha256', 5)))),
        namedtype.NamedType('objectId', univ.ObjectIdentifier())
    ))
    ),
    namedtype.NamedType('aliases', univ.SequenceOf(componentType=ResourceAlias())),
    namedtype.NamedType('dependencies', univ.SequenceOf(componentType=ResourceReference())),
    namedtype.OptionalNamedType('payload', PayloadDescription())
)


class Resource(univ.Sequence):
    pass


Resource.componentType = namedtype.NamedTypes(
    namedtype.OptionalNamedType('uri', Uri()),
    namedtype.NamedType('resourceType', univ.Enumerated(namedValues=namedval.NamedValues(('manifest', 0), ('payload', 1)))),
    namedtype.NamedType('resource', univ.Choice(componentType=namedtype.NamedTypes(
        namedtype.NamedType('manifest', Manifest()),
        namedtype.NamedType('payload', Payload())
    ))
    )
)


class SignedResource(univ.Sequence):
    pass


SignedResource.componentType = namedtype.NamedTypes(
    namedtype.NamedType('resource', Resource()),
    namedtype.NamedType('signature', ResourceSignature())
)
